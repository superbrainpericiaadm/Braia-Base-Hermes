# Proveniência da v1.0.11

A Braia Base nasceu da estrutura modular criada no commit
`f1d4c415b7c25483bcce0307b87fc29da531eb32`. A compatibilidade atual foi portada
seletivamente da release oficial:

- fonte: `superbrainpericiaadm/Braia-esc-pericias-Hermes`;
- tag: `v1.0.11`;
- commit: `fd6126aa06d357736942f0e801a732f6a754dfa2`;
- runtime Hermes homologado: árvore
  `59d8aa0a3099a0a74aab6f9abd2c4ffcc8ddf5d2`;
- patch cumulativo SHA256:
  `fbe6b92fcf4119c825d2ecc5546332c2e432736717810094f34430d926d9f5a7`.

Foram portados o contrato de roteamento por tarefa, os catálogos Claude e
ChatGPT/Codex, o configurador de assinaturas, o frontend PKCE do Claude, o
aplicador e os patches revisados do runtime. A identidade, a equipe de seis
agentes, os dois níveis de delegação, o sistema de módulos e o onboarding da
Braia Base foram preservados e adaptados ao novo contrato.

Não foram copiados agentes periciais, rotinas de clientes, cron, tokens,
credenciais, relatórios de laboratório, endereços de VPS ou o atualizador
seletivo da distribuição pericial. O Worker de provisionamento não faz parte
deste repositório nesta etapa.

A árvore do patch é fixa. `hermes_requires: >=0.21.0` expressa o mínimo funcional
da distribuição, mas `apply_runtime_patch.py` só aceita a árvore exata revisada.
Qualquer atualização upstream do Hermes exige nova adaptação e homologação.
