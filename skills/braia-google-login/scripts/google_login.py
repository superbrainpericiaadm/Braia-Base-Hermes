#!/usr/bin/env python3
"""Login Google da Braia sem copiar nada: o dono só autoriza no navegador.

Reaproveita o setup.py da skill bundled google-workspace (mesmos arquivos, mesmo formato de
token), trocando apenas o endereço de retorno: em vez de http://localhost:1, o Google devolve
o código ao portal da SuperBrain, e um esperador em segundo plano nesta VPS busca o código no
portal e conclui a troca pelo token. O portal guarda o código por poucos minutos e nunca vê o
token: o código só vale junto com o verificador PKCE, que fica só aqui.

Comandos (com o perfil ativo; HERMES_HOME é a raiz do perfil):
    python google_login.py start     imprime a URL para o dono e deixa o esperador rodando
    python google_login.py status    PENDENTE | AUTENTICADO | ERRO <motivo> | NADA
    python google_login.py wait      uso interno (esperador)
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PORTAL = "https://instalar.superbrainpericia.com.br"
PORTAL_REDIRECT = f"{PORTAL}/api/google/retorno"
WAIT_MINUTES = 15
POLL_SECONDS = 4


def hermes_home() -> Path:
    return Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes").expanduser()


HOME = hermes_home()
STATUS_PATH = HOME / "google_login_status.json"
LOG_PATH = HOME / "google_login.log"
SETUP_DIR = HOME / "skills" / "productivity" / "google-workspace" / "scripts"


def log(msg: str) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}\n")


def set_status(status: str, detail: str = "") -> None:
    STATUS_PATH.write_text(json.dumps({"status": status, "detail": detail, "at": datetime.now().isoformat(timespec="seconds")}), encoding="utf-8")


def load_setup():
    """Importa o setup.py bundled como módulo, com o retorno apontando para o portal."""
    if not (SETUP_DIR / "setup.py").exists():
        raise SystemExit("ERRO: skill bundled google-workspace ausente no perfil. O gateway sincroniza as skills ao subir; tente de novo em um minuto.")
    sys.path.insert(0, str(SETUP_DIR))
    import setup as gsetup  # noqa: E402

    gsetup.REDIRECT_URI = PORTAL_REDIRECT
    return gsetup


def client_kind(gsetup) -> str:
    data = json.loads(gsetup.CLIENT_SECRET_PATH.read_text(encoding="utf-8"))
    return "web" if "web" in data else "installed"


def cmd_start() -> None:
    gsetup = load_setup()
    if not gsetup.CLIENT_SECRET_PATH.exists():
        raise SystemExit("ERRO: cliente OAuth da Braia não registrado no perfil. Rode antes: setup.py --client-secret ${HERMES_HOME}/google_client_secret.json")
    if client_kind(gsetup) != "web":
        # cliente antigo (aplicativo para computador): o Google só aceita localhost, então não há retorno no portal
        raise SystemExit("ERRO: o cliente OAuth instalado é do tipo antigo; peça à SuperBrain a atualização da distribuição.")
    gsetup.get_auth_url()  # imprime a URL e grava google_oauth_pending.json com o retorno no portal
    set_status("pending")
    log("start: URL gerada, esperador iniciado")
    with LOG_PATH.open("a", encoding="utf-8") as out:
        subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), "wait"],
            stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT,
            start_new_session=True, close_fds=True, env=os.environ.copy(),
        )


def cmd_wait() -> None:
    gsetup = load_setup()
    pending = gsetup._load_pending_auth()
    state = pending["state"]
    deadline = time.time() + WAIT_MINUTES * 60
    while time.time() < deadline:
        # o pendente foi trocado por outro start: este esperador sai
        try:
            if json.loads(gsetup.PENDING_AUTH_PATH.read_text(encoding="utf-8")).get("state") != state:
                log("wait: pendente substituído, encerrando")
                return
        except Exception:
            log("wait: pendente removido, encerrando")
            return
        try:
            req = Request(f"{PORTAL}/api/google/codigo?{urlencode({'state': state})}", headers={"User-Agent": "braia-google-login"})
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            if e.code != 404:
                log(f"wait: portal respondeu {e.code}")
            time.sleep(POLL_SECONDS)
            continue
        except (URLError, TimeoutError, ValueError) as e:
            log(f"wait: portal indisponível ({e})")
            time.sleep(POLL_SECONDS * 3)
            continue
        if data.get("error"):
            set_status("error", data["error"])
            log(f"wait: Google recusou ({data['error']})")
            return
        params = {"code": data["code"], "state": state}
        if data.get("scope"):
            params["scope"] = data["scope"]
        callback = f"{PORTAL_REDIRECT}?{urlencode(params)}"
        try:
            gsetup.exchange_auth_code(callback)
        except SystemExit as e:
            set_status("error", f"troca do código falhou (código {e.code})")
            log("wait: troca do código falhou")
            return
        set_status("authenticated")
        log("wait: token gravado")
        return
    set_status("error", "o dono não autorizou em 15 minutos")
    log("wait: tempo esgotado")


def cmd_status() -> None:
    if not STATUS_PATH.exists():
        print("NADA")
        return
    data = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    status = data.get("status")
    if status == "authenticated":
        print("AUTENTICADO")
    elif status == "pending":
        print("PENDENTE")
    else:
        print(f"ERRO {data.get('detail', '')}".strip())


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "start":
        cmd_start()
    elif cmd == "wait":
        cmd_wait()
    elif cmd == "status":
        cmd_status()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
