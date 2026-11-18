"""Adversarial filewise/runtime concurrency tests for the v1.0.11 helper."""
import importlib.util
from pathlib import Path
import subprocess

import pytest

REPO = Path(__file__).resolve().parents[1]
BASE = b"value = 1\n" + b"# context\n" * 12
TARGET = BASE.replace(b"value = 1", b"value = 3")
MANAGED = ("tools/delegate_tool.py", "hermes_cli/config_defaults.py")


def run_git(root, *args):
    return subprocess.check_output(
        ["git", "-c", "core.autocrlf=false", "-C", str(root), *args], text=True
    ).strip()


@pytest.fixture
def lab(tmp_path):
    spec = importlib.util.spec_from_file_location("audited_runtime_helper", REPO / "scripts/apply_runtime_patch.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    for rel in MANAGED:
        path = runtime / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(BASE)
    (runtime / "hermes_cli" / "__init__.py").write_text('__version__ = "0.21.0"\n', encoding="utf-8")
    (runtime / ".gitignore").write_text("*.ignored\n", encoding="utf-8")
    run_git(runtime, "init", "-q")
    run_git(runtime, "add", "-A")
    run_git(runtime, "-c", "user.name=Lab", "-c", "user.email=lab@example.invalid", "commit", "-qm", "base")
    base_tree = run_git(runtime, "rev-parse", "HEAD^{tree}")
    helper.KNOWN_BASE_TREES = {"0.21.0": (base_tree,)}
    patch = tmp_path / "target.patch"
    for rel in MANAGED:
        (runtime / rel).write_bytes(TARGET)
    patch.write_bytes(subprocess.check_output(["git", "-C", str(runtime), "diff", "--no-ext-diff"]))
    run_git(runtime, "restore", "--", *MANAGED)
    return helper, runtime, patch, tmp_path / "backups"


@pytest.mark.parametrize("kind", ["tracked", "untracked", "ignored", "staged"])
def test_unowned_git_state_neither_blocks_nor_enters_payload(lab, kind):
    helper, runtime, patch, backups = lab
    suffix = "ignored" if kind == "ignored" else "txt"
    extra = runtime / f"customer-{kind}.{suffix}"
    extra.write_bytes(f"preserve-{kind}\n".encode())
    if kind in {"tracked", "staged"}:
        run_git(runtime, "add", extra.name)
    if kind == "tracked":
        run_git(runtime, "-c", "user.name=Lab", "-c", "user.email=lab@example.invalid", "commit", "-qm", "unowned")
    original = extra.read_bytes()
    assert helper.install(runtime, patch, backups, check=True)["status"] == "ready"
    result = helper.install(runtime, patch, backups)
    assert result["status"] == "applied"
    assert extra.read_bytes() == original
    assert all((runtime / rel).read_bytes() == TARGET for rel in MANAGED)


def test_clean_three_way_preserves_local_and_release(lab):
    helper, runtime, patch, backups = lab
    path = runtime / MANAGED[0]
    path.write_bytes(BASE + b"customer_extension = True\n")
    assert helper.install(runtime, patch, backups)["status"] == "applied"
    merged = path.read_bytes()
    assert b"value = 3" in merged
    assert b"customer_extension = True" in merged


def test_unowned_commit_mid_check_does_not_block(lab, monkeypatch):
    helper, runtime, patch, backups = lab
    original_snapshot = helper._snapshot
    injected = False

    def snapshot_then_commit(root, names):
        nonlocal injected
        result = original_snapshot(root, names)
        if not injected:
            injected = True
            extra = runtime / "customer-unowned.py"
            extra.write_text("customer = True\n", encoding="utf-8")
            run_git(runtime, "add", extra.name)
            run_git(runtime, "-c", "user.name=Lab", "-c", "user.email=lab@example.invalid", "commit", "-qm", "unowned concurrent")
        return result

    monkeypatch.setattr(helper, "_snapshot", snapshot_then_commit)
    assert helper.install(runtime, patch, backups, check=True)["status"] == "ready"
    assert all((runtime / rel).read_bytes() == BASE for rel in MANAGED)
    assert not backups.exists()


@pytest.mark.parametrize("case", ["same-line-conflict", "deletion-conflict", "unknown-base"])
def test_refusal_precedes_backup_and_effects(lab, case):
    helper, runtime, patch, backups = lab
    before = {rel: (runtime / rel).read_bytes() for rel in MANAGED}
    if case == "same-line-conflict":
        (runtime / MANAGED[0]).write_bytes(BASE.replace(b"value = 1", b"value = 99"))
    elif case == "deletion-conflict":
        (runtime / MANAGED[0]).unlink()
    else:
        helper.KNOWN_BASE_TREES = {"9.9.9": ("0" * 40,)}
    observed = {rel: ((runtime / rel).read_bytes() if (runtime / rel).exists() else None) for rel in MANAGED}
    with pytest.raises(ValueError):
        helper.install(runtime, patch, backups)
    assert {rel: ((runtime / rel).read_bytes() if (runtime / rel).exists() else None) for rel in MANAGED} == observed
    assert not backups.exists()
    if case == "unknown-base":
        assert observed == before
