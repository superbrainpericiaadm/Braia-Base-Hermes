# Homologação da Braia Base v1.0.11

A homologação combina testes da distribuição e prova contra a árvore exata do
Hermes. Testes unitários não comprovam inferência, Telegram ou consumo do plano.

## Estrutural

- `distribution.yaml` e `product.yaml` em `1.0.11`;
- nenhum segredo, banco, cliente OAuth ou dado de cliente no Git;
- configuração com `braia_routing` schema 1 e sem A/B/C ou pin estático de filho;
- profundidade 1, Braia na raiz e todos os especialistas como folhas;
- módulos adicionais preservados em `local/`;
- helper Claude usando o perfil atual e OAuth de assinatura;
- runtime patch idempotente e limitado à árvore revisada.

## Perfil isolado

Com dados fictícios, instale a tag, aplique o patch, conecte uma assinatura e
rode o configurador. Repita com Codex somente, Claude somente e as duas contas,
com preferência inicial de cada família. Confirme:

1. primeira configuração e reaplicação idempotente;
2. Braia usando `action="route"` antes do filho direto;
3. Braia delegando diretamente até três folhas, inclusive com modelos diferentes
   dentro da mesma família ativa, sem permissão de nova delegação pelos filhos;
4. `execution_id`, conclusão síncrona e assíncrona e review vinculado à sessão;
5. fallback com capacidade equivalente ou superior e tentativas limitadas;
6. configuração, OAuth, memória, workspace, cron, módulos e SQLite preservados.

## Casos funcionais

| Pedido | Evidência esperada |
|---|---|
| Organize arquivos e peça ao Paulo um inventário | Braia decompõe a demanda e chama Juliana e Paulo diretamente como folhas; depois valida e consolida. |
| Davi, coordene SDRs ativos | Braia chama Davi como folha para gestão e chama diretamente cada SDR necessário; só skills registradas são usadas. |
| Revise meu laudo com Rebeca | Sem módulo ativo, informa a capacidade ausente. |
| Conecte meu Claude | Link PKCE na conversa privada, código sem eco, configuração preservada e inferência separada. |
| Agende reunião sem data | Isaura informa a lacuna; não cria evento. |

Teste de modelo real exige conta própria do laboratório. Teste Google exige
cliente OAuth provisionado fora do Git. Telegram exige bot dedicado, allowlist e
destino autorizado. Nenhuma dessas integrações é ativada pelo simples clone.
