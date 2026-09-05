# Proveniência

Derivação em 2026-09-05, a partir de:

- Repositório: https://github.com/superbrainpericiaadm/Braia-esc-pericias-Hermes
- Branch consultada: main
- Commit: fe8c312522608d9146bff571da3259eb82cb9717
- Versão declarada na origem: 1.0.10
- Hermes consultado localmente: 0.20.4, commit b2057c16856fc01eeb17a40aa65853a68e61b981.

Reaproveitados: estrutura de distribuição, configuração geral de voz/memória/modelo,
contrato de repasse e helper de login Google. Reescritos: identidade, governança,
roster, agentes do núcleo, onboarding e integração de adicionais.
Não copiados: credenciais, histórico Git, Rebeca, Rogério, suas bases técnicas,
Alexandre, rotinas de clientes ou monitor externo de cota.

Delegação em camadas foi conferida no código tools/delegate_tool.py e na
[documentação oficial](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation/).
Uso de distribution_owned e preservação foi conferido em hermes_cli/profile_distribution.py.
O mínimo 0.20.4 é a referência adotada para esta base; não significa que toda
versão futura foi homologada. Mudanças posteriores na origem exigem revisão e
portabilidade seletiva; não há sincronização automática com a distribuição pericial.
