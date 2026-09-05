# Braia Base v1.0.11

Esta release torna a Braia Base compatível com o contrato técnico da Braia
v1.0.11 e mantém a arquitetura modular própria do produto.

## Mudanças

- cada subtarefa recebe modelo e esforço conforme complexidade, dentro do
  provedor ativo;
- uma assinatura ChatGPT/Codex ou Claude basta, e a segunda oferece fallback
  capaz e prioridade adaptativa baseada em entregas aceitas;
- preferência manual do dono prevalece e falha isolada não muda a ordem;
- login Claude pode ser conduzido pela conversa privada com OAuth de assinatura,
  sem API key, terminal para o cliente ou ativação de uso extra;
- o runtime registra `execution_id`, conclusão síncrona ou assíncrona e review
  vinculado à evidência;
- o patch cumulativo e o configurador revisado acompanham a distribuição;
- módulos, OAuth, Google, workspace, memórias, sessões e configurações locais
  continuam fora do conteúdo substituível da distribuição.

A Braia Base preserva dois níveis de execução. A Braia escolhe a prioridade do
provedor e despacha Juliana ou Davi como orquestradores. Eles selecionam modelos
dos filhos dentro da mesma família ativa e os despacham como folhas. Agente e
skill definem responsabilidade e método; o nome do agente não fixa a LLM.

## Proveniência

O contrato foi portado da release oficial `Braia-esc-pericias-Hermes/v1.0.11`,
commit `fd6126aa06d357736942f0e801a732f6a754dfa2`. O patch cumulativo mantém SHA256
`fbe6b92fcf4119c825d2ecc5546332c2e432736717810094f34430d926d9f5a7` e aceita
somente a árvore Hermes revisada
`59d8aa0a3099a0a74aab6f9abd2c4ffcc8ddf5d2`.

## Validação

- Windows: 90 testes aprovados, 1 ignorado e 12 subtestes aprovados;
- Linux no pacote fechado: 91 testes aprovados e 12 subtestes aprovados;
- runtime Hermes real após o patch: 202 testes aprovados e zero falhas;
- patch comprovado nos estados `ready`, `applied` e `already_applied`;
- instalação real da distribuição confirmou versão 1.0.11, profundidade 2,
  skill Claude e preservação de sentinelas em workspace, memória e `local/`.

Os transportes de modelo, Google e Telegram não foram acionados por esta
validação. A integração de modelos da v1.0.11 já foi homologada na distribuição
de origem, mas a Braia Base ainda exige smoke test com as contas e canais de
cada ambiente. O Worker que escolherá a primeira assinatura em instalações
novas será integrado em outra etapa.
