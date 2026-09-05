import importlib.util
import json
import os
from pathlib import Path
import re
import shutil

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


setup = load('profile_setup')
modules = load('module_manager')


@pytest.fixture
def profile(tmp_path):
    dest = tmp_path / 'custom-profile'
    dest.mkdir()
    for name in ['distribution.yaml', 'product.yaml', 'AGENTS.md', 'config.yaml']:
        shutil.copy2(ROOT / name, dest / name)
    shutil.copytree(ROOT / 'skills', dest / 'skills')
    return dest


@pytest.fixture
def package(tmp_path):
    dest = tmp_path / 'sample-package'
    path = dest / 'skills' / 'agente-catalogador'
    path.mkdir(parents=True)
    (path / 'SKILL.md').write_text('---\nname: agente-catalogador\ndescription: Catalogar documentos locais.\n---\nOrganize o inventário solicitado e retorne ao chamador.\n', encoding='utf-8')
    manifest = {'id': 'catalogador', 'version': '0.1.0', 'base_requires': '>=0.1.0,<0.2.0',
                'kind': 'agent', 'skills': ['agente-catalogador'],
                'agents': [{'name': 'Catalogador', 'skill': 'agente-catalogador', 'role': 'leaf', 'domain': 'Inventário local.'}]}
    (dest / 'module.yaml').write_text(yaml.safe_dump(manifest), encoding='utf-8')
    return dest


def edit_manifest(package, **changes):
    path = package / 'module.yaml'
    manifest = yaml.safe_load(path.read_text(encoding='utf-8'))
    manifest.update(changes)
    path.write_text(yaml.safe_dump(manifest), encoding='utf-8')


def test_package_core_and_skill_references():
    files = list((ROOT / 'skills').glob('*/SKILL.md'))
    slugs = {p.parent.name for p in files}
    assert slugs == modules.CORE
    assert {s for s in slugs if s.startswith('agente-')} == {
        'agente-juliana-ops', 'agente-isaura', 'agente-paulo-dev', 'agente-angelica', 'agente-davi-sdr'}
    for path in files:
        text = path.read_text(encoding='utf-8')
        fm = yaml.safe_load(text.split('---', 2)[1])
        assert fm['name'] == path.parent.name
        assert fm['description']
        for ref in re.findall(r'skill_view\([\'"]([a-z0-9-]+)[\'"]\)', text):
            assert ref in slugs or ref == 'google-workspace'


def test_distribution_owns_no_customer_paths():
    manifest = yaml.safe_load((ROOT / 'distribution.yaml').read_text(encoding='utf-8'))
    product = yaml.safe_load((ROOT / 'product.yaml').read_text(encoding='utf-8'))
    assert manifest['version'] == product['version']
    assert not {'local', 'workspace', 'cron', 'auth.json', '.env', 'google_token.json',
                'google_client_secret.json'} & set(manifest['distribution_owned'])
    assert all((ROOT / p).exists() for p in manifest['distribution_owned'])
    config = yaml.safe_load((ROOT / 'config.yaml').read_text(encoding='utf-8'))
    assert config['delegation']['max_spawn_depth'] == 2
    assert config['delegation']['orchestrator_enabled'] is True
    assert '${HERMES_HOME}/local/skills' in config['skills']['external_dirs']
    assert not any(config['skills']['config']['braia'].values())


def test_setup_custom_path_preserves_customer_state(profile):
    manifest_path = profile / 'distribution.yaml'
    manifest = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))
    manifest['name'] = 'custom-profile'
    manifest_path.write_text(yaml.safe_dump(manifest), encoding='utf-8')
    setup.setup(profile)
    config_path = profile / 'config.yaml'
    config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
    config['model'] = {'default': 'client-model', 'provider': 'client-provider'}
    config['skills']['config']['braia']['owner_name'] = 'Cliente de teste'
    config_path.write_text(yaml.safe_dump(config), encoding='utf-8')
    (profile / 'workspace' / 'regras-empresa.md').write_text('Regra do cliente', encoding='utf-8')
    (profile / '.env').write_text('SENTINEL=private-test', encoding='utf-8')
    setup.setup(profile)
    config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
    assert config['terminal']['cwd'] == str(profile / 'workspace')
    assert config['model']['default'] == 'client-model'
    assert config['skills']['config']['braia']['owner_name'] == 'Cliente de teste'
    assert (profile / 'workspace' / 'regras-empresa.md').read_text(encoding='utf-8') == 'Regra do cliente'
    assert (profile / '.env').read_text(encoding='utf-8') == 'SENTINEL=private-test'


def test_governance_update_and_local_conflict(profile):
    setup.setup(profile)
    distributed = profile / 'AGENTS.md'
    distributed.write_text('Nova governança', encoding='utf-8')
    setup.setup(profile)
    target = profile / 'workspace' / 'AGENTS.md'
    assert target.read_text(encoding='utf-8') == 'Nova governança'
    assert list((profile / 'backups' / 'governance').glob('*.md'))
    target.write_text('Regra local editada', encoding='utf-8')
    with pytest.raises(ValueError, match='local foi editado'):
        setup.setup(profile)
    assert target.read_text(encoding='utf-8') == 'Regra local editada'
    setup.setup(profile, accept_governance=True)
    assert target.read_text(encoding='utf-8') == 'Nova governança'


def test_install_module_and_preserve_on_setup(profile, package):
    setup.setup(profile)
    modules.install(package, profile)
    registry_before = (profile / 'local' / 'module-registry.json').read_bytes()
    setup.setup(profile)
    assert (profile / 'local' / 'module-registry.json').read_bytes() == registry_before
    registry = json.loads(registry_before)
    assert registry['modules']['catalogador']['status'] == 'active'
    assert (profile / 'local' / 'skills' / 'agente-catalogador' / 'SKILL.md').is_file()
    with pytest.raises(ValueError, match='já instalado'):
        modules.install(package, profile)
    assert not (profile / 'local' / 'module-install.lock').exists()


@pytest.mark.parametrize('changes', [
    {'id': '../outside'}, {'skills': ['../outside']}, {'base_requires': '>=0.2.0'},
    {'version': 'broken'}, {'base_requires': 'latest'}, {'kind': 'unknown'},
    {'skills': ['agente-paulo-dev']}, {'skills': ['agente-catalogador', 'agente-catalogador']},
    {'agents': [{'name': 'Bad', 'skill': 'missing', 'role': 'leaf', 'domain': 'x'}]},
    {'agents': [{'name': 'Bad', 'skill': 'agente-catalogador', 'role': 'orchestrator', 'domain': 'x'}]},
])
def test_reject_invalid_packages_without_mutation(profile, package, changes):
    edit_manifest(package, **changes)
    with pytest.raises(ValueError):
        modules.install(package, profile)
    assert not (profile / 'local').exists()


def test_reject_existing_skill(profile, package):
    existing = profile / 'skills' / 'agente-catalogador'
    existing.mkdir()
    (existing / 'SKILL.md').write_text('Existing skill', encoding='utf-8')
    with pytest.raises(ValueError, match='Colisão'):
        modules.install(package, profile)
    assert (existing / 'SKILL.md').read_text(encoding='utf-8') == 'Existing skill'


def test_install_tool_module(profile, package):
    edit_manifest(package, kind='tool', agents=[])
    result = modules.install(package, profile)
    assert result['kind'] == 'tool'


def test_reject_links(profile, package, tmp_path):
    outside = tmp_path / 'outside.txt'
    outside.write_text('not package data', encoding='utf-8')
    link = package / 'skills' / 'agente-catalogador' / 'outside.txt'
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip('Symlink creation requires OS permission')
    with pytest.raises(ValueError, match='Links simbólicos'):
        modules.install(package, profile)


def test_install_rolls_back_on_registry_write_failure(profile, package, monkeypatch):
    original = Path.replace
    def fail_registry(self, target):
        if Path(target).name == 'module-registry.json':
            raise OSError('simulated disk failure')
        return original(self, target)
    monkeypatch.setattr(Path, 'replace', fail_registry)
    with pytest.raises(OSError, match='simulated'):
        modules.install(package, profile)
    assert not (profile / 'local' / 'skills' / 'agente-catalogador').exists()
    assert not list((profile / 'local').glob('.module-stage-*'))
    assert not (profile / 'local' / 'module-install.lock').exists()


def test_exclusive_lock_does_not_remove_other_installer_lock(profile, package):
    local = profile / 'local'
    local.mkdir()
    lock = local / 'module-install.lock'
    lock.write_text('another-process', encoding='utf-8')
    with pytest.raises(FileExistsError):
        modules.install(package, profile)
    assert lock.read_text(encoding='utf-8') == 'another-process'
