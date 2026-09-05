#!/usr/bin/env python3
"""Prepare a Braia profile without replacing client data or edited governance."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml


def digest(data):
    return hashlib.sha256(data).hexdigest()


def setup(profile, accept_governance=False):
    profile = Path(profile).expanduser().resolve(strict=True)
    manifest = yaml.safe_load((profile / 'product.yaml').read_text(encoding='utf-8'))
    if manifest.get('id') != 'braia-base':
        raise ValueError('O destino não é um perfil braia-base.')
    config_path = profile / 'config.yaml'
    config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
    if not isinstance(config, dict):
        raise ValueError('config.yaml inválido.')
    workspace = profile / 'workspace'
    local = profile / 'local'
    for folder in [workspace, local, local / 'skills']:
        folder.mkdir(parents=True, exist_ok=True)
    state_path = local / 'base-setup.json'
    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    source = (profile / 'AGENTS.md').read_bytes()
    target = workspace / 'AGENTS.md'
    if target.exists() and target.read_bytes() != source:
        old = target.read_bytes()
        if digest(old) != state.get('governance_sha256') and not accept_governance:
            (local / 'AGENTS.distribution.pending.md').write_bytes(source)
            raise ValueError('AGENTS.md local foi editado. Revise local/AGENTS.distribution.pending.md; '
                             'use --accept-governance após conciliar as regras locais.')
        backups = profile / 'backups' / 'governance'
        backups.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        (backups / f'AGENTS-{stamp}.md').write_bytes(old)
    target.write_bytes(source)
    config.setdefault('terminal', {})['cwd'] = str(workspace)
    dirs = config.setdefault('skills', {}).setdefault('external_dirs', [])
    path = '${HERMES_HOME}/local/skills'
    if path not in dirs and str(local / 'skills') not in dirs:
        dirs.append(path)
    config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding='utf-8')
    registry = local / 'module-registry.json'
    if not registry.exists():
        registry.write_text('{"schema_version": 1, "modules": {}}\n', encoding='utf-8')
    rules = workspace / 'regras-empresa.md'
    if not rules.exists():
        rules.write_text('# Regras da empresa\n\nRegistrar aqui as regras específicas aprovadas pelo cliente.\n', encoding='utf-8')
    state_path.write_text(json.dumps({'governance_sha256': digest(source)}, indent=2) + '\n', encoding='utf-8')
    return workspace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--accept-governance', action='store_true')
    args = parser.parse_args()
    try:
        print(f'OK: workspace preparado em {setup(args.profile, args.accept_governance)}')
    except (OSError, ValueError, yaml.YAMLError) as exc:
        parser.exit(1, f'ERRO: {exc}\n')


if __name__ == '__main__':
    main()
