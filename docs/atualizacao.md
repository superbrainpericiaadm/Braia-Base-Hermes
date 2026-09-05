# Atualização e rollback

O núcleo evolui em Braia-Base-Hermes. Revisar mudanças, rodar testes e homologar
em perfil separado antes de promover para clientes. A origem pericial continua
independente; importar correções por revisão, sem merge automático de conteúdo vertical.

1. Parar o gateway em uma janela de manutenção.
2. Fazer backup completo e privado da raiz do perfil, incluindo configuração,
   credenciais, local, workspace e cron, antes de qualquer alteração.
3. Registrar commit/versão atual e executar `hermes profile update braia-base`.
4. Executar `scripts/profile_setup.py --profile /RAIZ/ABSOLUTA/DO/PERFIL`.
5. Conferir config, registro de módulos, skills disponíveis e uma tarefa local.
6. Reiniciar o gateway após validação.

O update normal preserva config.yaml. O setup muda somente cwd, diretório externo
de skills e governança gerenciada, mantendo configurações e dados do cliente.
Se um AGENTS.md local foi editado fora do setup, ele recusa sobrescrever: guarda a
versão proposta em local/AGENTS.distribution.pending.md para revisão. Após conciliar,
o instalador pode usar `--accept-governance`, que salva backup da versão anterior.
Regras particulares devem ficar em workspace/regras-empresa.md.

Não usar --force-config em uma atualização rotineira: ele substitui ajustes locais.
Comparar mudanças de configuração distribuída manualmente. Na primeira instalação,
max_spawn_depth=2 e orchestrator_enabled=true já vêm configurados. Em migração de
outro perfil, conferir esses campos explicitamente; o setup não força permissões.

Para releases controladas, usar clone local em tag/commit aprovado como fonte de
instalação. Não depender do HEAD móvel de main para reproduzir uma entrega.
O rollback restaura o backup completo do perfil, com gateway parado, e a versão
anterior da distribuição. Não aplicar instalação --force sobre dados sem backup.

distribution_owned explicita o que o pacote atualiza. local/, workspace/, memória,
credenciais e cron não pertencem à distribuição. Módulos comerciais têm ciclo de
versão próprio. Não substituir dados do cliente por conteúdo de teste.
