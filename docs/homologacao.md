# Homologação

Testes automatizados locais verificam estrutura, nomes de skills, instalação de
módulos, rejeição de colisões, validação de caminho e preservação no setup.
Eles não provam a qualidade das respostas de um modelo ou autenticação dos canais.

Em perfil isolado, com modelo autenticado e dados fictícios:

| Pedido | Evidência esperada |
|---|---|
| Quem é você? | Braia, equipe Base, sem identidade de outra empresa. |
| Juliana, organize estes arquivos e peça ao Paulo um script de inventário. | Braia chama Juliana como orchestrator; Juliana chama Paulo como leaf e valida arquivo/teste. |
| Davi, organize nosso funil. | Davi entrega gestão; não inventa SDRs instalados. |
| Davi, coordene os SDRs de teste instalados. | Braia chama Davi diretamente; SDRs folhas devolvem ao gerente. |
| Revise meu laudo com a Rebeca. | Sem adicional ativo: informa capacidade ausente e proposta de contratação. |
| Crie um agente para catalogar documentos locais. | Angélica prepara, valida e registra pacote autorizado. |
| Agende uma reunião sem data definida. | Isaura devolve a lacuna; não inventa evento. |

Conferir no trace do Hermes os papéis e profundidades, não só o texto da resposta.
Testar update com configuração, memória, módulo e documento sentinela e confirmar
preservação. Google: provisionar cliente OAuth local e realizar consentimento e
check. Telegram: bot dedicado e allowlist. Envio só com tarefa de teste autorizada.

## Evidência inicial, 2026-09-05

- `python -m pytest -q`: 20 testes aprovados no Windows/Python local.
- Instalação com `install_distribution` e atualização com `update_distribution`
  do Hermes 0.20.4 real, em HERMES_HOME temporário e nome de perfil alternativo:
  aprovadas. Setup e instalação de um agente fictício também executados.
- Confirmada a preservação de configuração do cliente, documento no workspace,
  memória, arquivo de ambiente fictício, cron e módulo local após update.
- Compilação dos scripts Python aprovada. Frontmatter validado conforme o formato
  Hermes (que inclui author/version, diferente do validador de skills Codex).

Estado inicial: em desenvolvimento. Conversas com modelo real, delegação observada
em trace, OAuth e Telegram ainda dependem da homologação no ambiente de execução.
