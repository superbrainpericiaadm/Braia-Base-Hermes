import hashlib
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(name):
    return yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))


def test_release_and_runtime_contract():
    distribution = load_yaml("distribution.yaml")
    product = load_yaml("product.yaml")
    assert distribution["version"] == product["version"] == "1.0.11"
    assert distribution["hermes_requires"] == ">=0.21.0"
    assert product["routing_contract"] == "braia-routing-v1"
    assert {"POLITICA-FALLBACK.md", "runtime-patches"} <= set(distribution["distribution_owned"])
    assert (ROOT / "docs/RELEASE-v1.0.11.md").is_file()
    patch = ROOT / "runtime-patches/delegation-fallback.patch"
    assert hashlib.sha256(patch.read_bytes()).hexdigest() == (
        "fbe6b92fcf4119c825d2ecc5546332c2e432736717810094f34430d926d9f5a7"
    )


def test_base_keeps_two_layers_with_dynamic_routing():
    cfg = load_yaml("config.yaml")
    assert cfg["delegation"]["max_spawn_depth"] == 2
    assert cfg["delegation"]["orchestrator_enabled"] is True
    assert cfg["delegation"]["child_timeout_seconds"] == 0
    assert not ({"provider", "model", "fallback_providers"} & set(cfg["delegation"]))
    policy = cfg["braia_routing"]
    assert policy["enabled"] is True and policy["initialized"] is False
    assert policy["schema_version"] == 1 and policy["policy_version"] == "braia-routing-v1"
    assert policy["learning"]["min_samples"] == 8
    assert policy["learning"]["sustained_windows"] == 2
    assert policy["fallback"]["max_attempts"] == 2


def test_configurator_preserves_base_two_layer_contract():
    sys.path.insert(0, str(ROOT / "scripts"))
    from configure_multi_ai import build_config

    catalog = {"openai-codex": {"models": {
        "gpt-5.6-luna": {"tier": "routine", "efforts": ["low", "medium", "high"], "default_effort": "medium"},
        "gpt-5.6-terra": {"tier": "normal", "efforts": ["low", "medium", "high"], "default_effort": "medium"},
        "gpt-5.6-sol": {"tier": "complex", "efforts": ["low", "medium", "high"], "default_effort": "medium"},
        "gpt-6-astra": {"tier": "exceptional", "efforts": ["medium", "high"], "default_effort": "medium"},
    }}}
    configured, mode = build_config(load_yaml("config.yaml"), True, False, catalog)
    assert mode == "DYNAMIC_ROUTING"
    assert configured["delegation"]["max_spawn_depth"] == 2
    assert configured["delegation"]["orchestrator_enabled"] is True
    assert configured["braia_routing"]["initialized"] is True


def test_prompts_describe_root_and_nested_routing():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    soul = (ROOT / "SOUL.md").read_text(encoding="utf-8")
    juliana = (ROOT / "skills/agente-juliana-ops/SKILL.md").read_text(encoding="utf-8")
    davi = (ROOT / "skills/agente-davi-sdr/SKILL.md").read_text(encoding="utf-8")
    assert 'action="route"' in agents
    assert 'role="orchestrator"' in agents and '"role": "leaf"' in agents
    assert "execution_id" in agents and "review" in agents
    assert "mesma família ativa" in juliana and "mesma família" in davi
    assert "braia-claude-login" in soul and "não fornece API key" in soul


def test_claude_and_config_helpers_target_base_profile():
    configure = (ROOT / "scripts/configure_multi_ai.py").read_text(encoding="utf-8")
    login = (ROOT / "skills/braia-claude-login/scripts/claude_login.py").read_text(encoding="utf-8")
    skill = (ROOT / "skills/braia-claude-login/SKILL.md").read_text(encoding="utf-8")
    for text in (configure, login):
        assert ".hermes/profiles/braia-base" in text
        assert ".hermes/profiles/braia-pericias" not in text
    assert "category: braia-base" in skill
    assert "API key" in skill and "uso extra" in skill


def test_core_skills_are_at_release_version():
    for path in (ROOT / "skills").glob("*/SKILL.md"):
        frontmatter = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        assert str(frontmatter["version"]) == "1.0.11", path


def test_repository_contains_no_credentials_or_lab_identifiers():
    patterns = [
        re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]+"),
        re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
        re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}\b"),
        re.compile(r"179\.199\.139\.199"),
        re.compile(r"luchettapericias\.com", re.IGNORECASE),
    ]
    excluded = {".git"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or excluded & set(path.parts) or path.suffix == ".pyc":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not any(pattern.search(text) for pattern in patterns), path
