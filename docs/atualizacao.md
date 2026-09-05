# Atualização para o contrato v1.0.11

A atualização da Braia Base é individual, com tag fixa e perfil ocioso. Não use
HEAD móvel, `--force-config` nem cópia integral sobre o perfil. O Worker de novas
instalações será tratado em outra etapa.

## Preservar

Antes de qualquer mudança, inventarie e faça backup privado de `config.yaml`,
`.env`, OAuth, Google, `local/`, `workspace/`, memórias, sessões, bancos, cron,
settings, nome, marca e integrações. Refresh tokens podem mudar durante uma
validação; não restaure credenciais antigas por reflexo.

O setup preserva dados e módulos. Se o `workspace/AGENTS.md` tiver edição local
fora do estado gerenciado, ele grava a proposta em
`local/AGENTS.distribution.pending.md` e interrompe. Concilie as regras e use
`--accept-governance` somente depois de revisar e guardar o backup.

## Ordem

1. Resolva caminhos absolutos do perfil, runtime, kit antigo, kit `v1.0.11` e
   backup. Confirme a árvore do runtime e a versão instalada.
2. Pare gateway e processos que leem o runtime.
3. Rode `apply_runtime_patch.py --check`; qualquer árvore ou alvo divergente
   bloqueia a atualização sem modificação.
4. Aplique o patch e guarde o manifesto do backup criado.
5. Atualize o perfil a partir do clone local na tag `v1.0.11`.
6. Rode `profile_setup.py` para atualizar a governança sem perder o namespace
   local.
7. Com `HERMES_HOME` apontando para o perfil e `PYTHONPATH` para o runtime, rode
   `configure_multi_ai.py --check` e depois sem `--check`.
8. Execute `hermes -p braia-base config check`, teste uma inferência na conta já
   conectada e só então reinicie o gateway.
9. Confira dados, módulos, modelo inicial, integrações e uma delegação com
   `routing` e `execution_id`.

Na migração de `0.1.0`, o configurador acrescenta `braia_routing`, aliases e
catálogo às configurações existentes, elimina pins estáticos de filhos e mantém
`max_spawn_depth: 2` e `orchestrator_enabled: true`. Uma assinatura basta. Não
inicie login Claude se o cliente não pediu; se ele pedir, a própria Braia usa
`braia-claude-login` na conversa privada.

## Falha

O aplicador de runtime aceita somente base limpa, patch predecessor revisado ou
a v1.0.11 já aplicada. Ele recusa symlinks, hardlinks, alterações locais e backup
dentro do runtime. Falha durante a transição restaura os bytes que ele próprio
alterou e preserva edições concorrentes para diagnóstico.

Rollback coordena código, configuração e serviço. Restaure uma versão anterior
somente com o gateway parado e evidência do estado atual. Nunca restaure OAuth ou
Google antigos sobre credenciais renovadas. Depois de qualquer rollback, rode uma
nova inspeção; ausência de saída não é sucesso.
