---
name: braia-onboarding
description: Configuração inicial da empresa e canais da Braia Base.
version: 1.0.11
author: SuperBrain Inteligência Pericial e Contábil Ltda
license: Proprietary
metadata:
  hermes:
    category: braia-base
    tags:
    - braia
    - braia-onboarding
---


# Onboarding

Confirme a raiz real do perfil e execute `scripts/profile_setup.py --profile` com
esse caminho absoluto. O script prepara workspace, governança e namespace local.
Leia `templates/onboarding.yaml` para os campos. Colete nome do responsável e da
empresa; peça os demais dados somente quando necessários à tarefa ou canal.
Não exigir CRC ou Corecon do produto base. Não copie dados de outra empresa.

Grave dados não secretos em `skills.config.braia` do config.yaml ativo. Preserve
modelo, provedor, credenciais e configurações que o instalador já definiu.
Registre regras específicas em `workspace/regras-empresa.md`, não no SOUL distribuído.

Para Telegram, confirme token local, allowlist e owner_telegram_id coerentes, com
o dono identificado. Para Google, siga `braia-google-login`. Não publique tokens.
Não ative cron, prospecção ou envio durante onboarding sem pedido correspondente.

Confira identidade da Braia, disponibilidade dos cinco especialistas e uma tarefa
local com Juliana. Relate o que está pronto e quais integrações não foram testadas.
