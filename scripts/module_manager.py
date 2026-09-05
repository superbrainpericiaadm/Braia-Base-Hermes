#!/usr/bin/env python3
"""Validate and install trusted local Braia modules; never execute package code."""
import argparse
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
VERSION = re.compile(r'^\d+\.\d+\.\d+$')
SPEC = re.compile(r'^(>=|<=|==|>|<)(\d+\.\d+\.\d+)$')
CORE = {'agente-juliana-ops', 'agente-isaura', 'agente-paulo-dev', 'agente-angelica',
        'agente-davi-sdr', 'equipe-braia-base', 'braia-orquestradora',
        'braia-onboarding', 'braia-google-login', 'braia-claude-login',
        'criar-agente-hermes'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def version_tuple(value):
    require(isinstance(value, str) and VERSION.fullmatch(value), 'Versão deve usar X.Y.Z.')
    return tuple(map(int, value.split('.')))


def compatible(version, spec):
    require(isinstance(spec, str) and spec.strip(), 'base_requires obrigatório.')
    current = version_tuple(version)
    matches = []
    for part in spec.split(','):
        match = SPEC.fullmatch(part.strip())
        require(match is not None, 'base_requires inválido; use comparadores X.Y.Z separados por vírgula.')
        op, target = match.groups()
        target = version_tuple(target)
        matches.append({'>=': current >= target, '<=': current <= target,
                        '>': current > target, '<': current < target, '==': current == target}[op])
    return all(matches)


def read_yaml(path):
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    require(isinstance(data, dict), f'Mapa YAML esperado: {path.name}')
    return data


def is_link(path):
    return path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction())


def validate(package, base_version='1.0.11'):
    package = Path(package).expanduser().absolute()
    require(not is_link(package), 'Pacote não pode ser link simbólico/junction.')
    package = package.resolve(strict=True)
    # os.walk does not descend directory symlinks. Reject them before inspecting payloads.
    for root, dirs, files in os.walk(package, followlinks=False):
        for name in dirs + files:
            require(not is_link(Path(root) / name), 'Links simbólicos/junctions não são aceitos em módulos.')
    manifest = read_yaml(package / 'module.yaml')
    module_id = manifest.get('id')
    require(isinstance(module_id, str) and len(module_id) <= 64 and SLUG.fullmatch(module_id), 'ID inválido.')
    version_tuple(manifest.get('version'))
    require(compatible(base_version, manifest.get('base_requires')), 'Módulo incompatível com a versão da base.')
    require(manifest.get('kind') in {'agent', 'tool'}, 'kind deve ser agent ou tool.')
    skills = manifest.get('skills')
    require(isinstance(skills, list) and skills, 'Lista skills vazia ou inválida.')
    require(all(isinstance(s, str) and len(s) <= 64 and SLUG.fullmatch(s) for s in skills), 'Slug de skill inválido.')
    require(len(skills) == len(set(skills)), 'Skills duplicadas.')
    require(not CORE.intersection(skills), 'Módulo tenta substituir skill do núcleo.')
    skills_root = package / 'skills'
    require(skills_root.is_dir(), 'Diretório skills ausente.')
    require({p.name for p in skills_root.iterdir()} == set(skills), 'Conteúdo de skills diverge do manifesto.')
    for slug in skills:
        path = skills_root / slug / 'SKILL.md'
        text = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        require(match is not None, f'Frontmatter ausente: {slug}')
        fm = yaml.safe_load(match.group(1))
        require(isinstance(fm, dict) and fm.get('name') == slug, f'name incorreto: {slug}')
        require(isinstance(fm.get('description'), str) and fm['description'].strip(), f'description ausente: {slug}')
        require(text[match.end():].strip(), f'Instruções vazias: {slug}')
    agents = manifest.get('agents')
    require(isinstance(agents, list), 'Lista agents obrigatória, mesmo vazia para ferramentas.')
    require(bool(agents) if manifest['kind'] == 'agent' else not agents, 'kind e agents divergentes.')
    for agent in agents:
        require(isinstance(agent, dict), 'Agente inválido.')
        require(agent.get('skill') in skills, 'Agente aponta para skill ausente.')
        require(agent.get('role') == 'leaf', 'Adicionais devem ser folhas.')
        require(all(isinstance(agent.get(k), str) and agent[k].strip() for k in ['name', 'domain']),
                'Nome e domínio obrigatórios.')
    require(len({a['skill'] for a in agents}) == len(agents), 'Agentes duplicados.')
    return manifest


def read_registry(profile):
    path = profile / 'local' / 'module-registry.json'
    registry = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'schema_version': 1, 'modules': {}}
    require(registry.get('schema_version') == 1 and isinstance(registry.get('modules'), dict), 'Registro inválido.')
    return registry


def install(package, profile):
    profile = Path(profile).expanduser().resolve(strict=True)
    base = read_yaml(profile / 'product.yaml')
    require(base.get('id') == 'braia-base', 'Destino não é braia-base.')
    manifest = validate(package, base['version'])
    package = Path(package).expanduser().resolve(strict=True)
    local = profile / 'local'
    local.mkdir(exist_ok=True)
    # Exclusive lock prevents two installers from racing over skills and registry.
    lock = local / 'module-install.lock'
    with lock.open('x', encoding='utf-8') as handle:
        handle.write(str(os.getpid()))
    installed = []
    stage = None
    pending = None
    try:
        registry = read_registry(profile)
        require(manifest['id'] not in registry['modules'], 'Módulo já instalado; atualização exige manutenção controlada.')
        skills_root = local / 'skills'
        skills_root.mkdir(exist_ok=True)
        existing = {p.parent.name for p in (profile / 'skills').rglob('SKILL.md')}
        existing.update(p.parent.name for p in skills_root.rglob('SKILL.md'))
        require(not existing.intersection(manifest['skills']), 'Colisão com skill existente.')
        for slug in manifest['skills']:
            require(not (skills_root / slug).exists(), 'Diretório de destino já existe.')
        stage = Path(tempfile.mkdtemp(prefix='.module-stage-', dir=local))
        for slug in manifest['skills']:
            shutil.copytree(package / 'skills' / slug, stage / slug)
        for slug in manifest['skills']:
            dest = skills_root / slug
            (stage / slug).rename(dest)
            installed.append(dest)
        registry['modules'][manifest['id']] = {
            **manifest, 'status': 'active',
            'installed_at': datetime.now(timezone.utc).isoformat(),
        }
        fd, temp_path = tempfile.mkstemp(prefix='.registry-', suffix='.json', dir=local)
        pending = Path(temp_path)
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(registry, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
        pending.replace(local / 'module-registry.json')
        return manifest
    except Exception:
        # Only remove directories this invocation just created, confined to the profile.
        for dest in installed:
            require(dest.resolve().parent == (local / 'skills').resolve(), 'Destino de rollback inválido.')
            shutil.rmtree(dest)
        raise
    finally:
        if stage is not None:
            require(stage.resolve().parent == local.resolve(), 'Destino de limpeza inválido.')
            shutil.rmtree(stage)
        if pending is not None and pending.exists():
            pending.unlink()
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    val = sub.add_parser('validate')
    val.add_argument('package', type=Path)
    val.add_argument('--base-version', default='1.0.11')
    add = sub.add_parser('install')
    add.add_argument('package', type=Path)
    add.add_argument('--profile', type=Path, required=True)
    listing = sub.add_parser('list')
    listing.add_argument('--profile', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            result = validate(args.package, args.base_version)
        elif args.command == 'install':
            result = install(args.package, args.profile)
        else:
            result = read_registry(args.profile.expanduser().resolve(strict=True))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        parser.exit(1, f'ERRO: {exc}\n')


if __name__ == '__main__':
    main()
