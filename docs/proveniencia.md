# Proveniência da v1.0.11

A Braia Base nasceu da estrutura modular criada no commit
`f1d4c415b7c25483bcce0307b87fc29da531eb32`. A compatibilidade atual foi portada
seletivamente da release oficial:

- fonte: `superbrainpericiaadm/Braia-esc-pericias-Hermes`;
- tag: `v1.0.11`;
- commit inicial: `fd6126aa06d357736942f0e801a732f6a754dfa2`;
- aplicador do runtime e seus testes sincronizados com a revisão da v1.0.11
  `86271a2c8b2bda527a6f6a4c5fb7fd33d33c6d82`, em 16/09/2026;
- runtime Hermes homologado: árvore
  `59d8aa0a3099a0a74aab6f9abd2c4ffcc8ddf5d2`;
- patch cumulativo SHA256:
  `fbe6b92fcf4119c825d2ecc5546332c2e432736717810094f34430d926d9f5a7`.

Foram portados o contrato de roteamento por tarefa, os catálogos Claude e
ChatGPT/Codex, o configurador de assinaturas, o frontend PKCE do Claude, o
aplicador e os patches revisados do runtime. A identidade, a equipe de seis
agentes, o sistema de módulos e o onboarding da Braia Base foram preservados.
A delegação foi alinhada ao contrato v1.0.11: Braia na raiz, uma camada de
especialistas folha e profundidade máxima 1.

Não foram copiados agentes periciais, rotinas de clientes, cron, tokens,
credenciais, relatórios de laboratório, endereços de VPS ou o atualizador
seletivo da distribuição pericial. O Worker de provisionamento é mantido em
repositório separado e deve fixar o commit deste pacote ao instalar a Base.

`hermes_requires: >=0.21.0` expressa o mínimo funcional da distribuição. O
aplicador reconhece as duas bases revisadas do Hermes 0.21.0: a árvore gerada
pelo instalador (`59d8aa0a3099a0a74aab6f9abd2c4ffcc8ddf5d2`) e a árvore upstream
(`daaffc303ae437041b7f76be17c5f61b14f2ce99`), ambas do código distribuído a partir
de `29112bef099274229cadff79cdff7bf7b99c4b77`. Ele preserva arquivos externos ao
patch e combina alterações locais compatíveis nos arquivos gerenciados.
Conflitos e alterações concorrentes nesses arquivos interrompem a aplicação.
Novas bases do Hermes exigem adaptação e validação próprias.
