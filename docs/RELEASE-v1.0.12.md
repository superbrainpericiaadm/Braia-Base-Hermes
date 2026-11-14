# Braia Base v1.0.12

Release de 14/11/2026. Base: v1.0.11 (`8eeac26`).

## Mudança

- O cliente OAuth Google do app da Braia (tipo aplicativo da Web, projeto
  `app-braia-504014`, client_id `941136456707-ehf3oeh1p783r21v1og02elfqs0dhth9`)
  passa a acompanhar a distribuição em
  `skills/braia-google-login/google_client_secret.json`, com exceção explícita
  no `.gitignore`. É o mesmo arquivo usado na v1.0.11 pelo instalador
  SuperBrain, sem alteração.
- O utilitário `skills/braia-google-login/scripts/google_login.py` segue
  **inalterado**: retorno no portal `instalar.superbrainpericia.com.br`,
  esperador em segundo plano, token gravado em `${HERMES_HOME}`.
- `SKILL.md` da `braia-google-login` indica onde está o cliente empacotado.

## Uso (Claude Code, com o perfil ativo)

```bash
install -m 600 "$HERMES_HOME/skills/braia-google-login/google_client_secret.json" "$HERMES_HOME/google_client_secret.json"
python "$HERMES_HOME/skills/productivity/google-workspace/scripts/setup.py" --install-deps
python "$HERMES_HOME/skills/productivity/google-workspace/scripts/setup.py" --client-secret "$HERMES_HOME/google_client_secret.json"
python "$HERMES_HOME/skills/braia-google-login/scripts/google_login.py" start
python "$HERMES_HOME/skills/braia-google-login/scripts/google_login.py" status
python "$HERMES_HOME/skills/productivity/google-workspace/scripts/setup.py" --check
```

## Segurança

Somente o JSON do cliente entra no repositório. Tokens (`google_token.json`),
pendências, logs e status continuam ignorados pelo Git e nunca fazem parte da
distribuição.
