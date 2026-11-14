---
name: equipe-braia-base
description: Equipe, responsabilidades e módulos ativos da Braia Base.
version: 1.0.12
author: SuperBrain Inteligência Pericial e Contábil Ltda
license: Proprietary
metadata:
  hermes:
    category: braia-base
    tags:
    - braia
    - equipe-braia-base
---


# Equipe da Braia Base

Braia orquestra e responde ao dono. O AGENTS.md do workspace é o contrato de execução.
Os agentes abaixo definem responsabilidade e método. O modelo é escolhido por
tarefa no catálogo do provedor ativo, conforme a política v1.0.11.

| Responsável | Skill | Entrega |
|---|---|---|
| Juliana | `agente-juliana-ops` | Operação executada e validada. |
| Isaura | `agente-isaura` | Atendimento, documentos, agenda e secretaria. |
| Paulo | `agente-paulo-dev` | Código, integração e automação testada. |
| Angélica | `agente-angelica` | Agente contratado, treinado e integrado. |
| Davi | `agente-davi-sdr` | Gestão comercial e coordenação de SDRs ativos. |

Antes de encaminhar a um adicional, leia `local/module-registry.json` na raiz do
perfil. Só estão ativos agentes em módulos com status `active` e skill realmente
disponível. Catálogo e registro ativo são coisas distintas. Não instalar ou acionar
Rebeca/Rogério apenas porque seus nomes aparecem na documentação.

Os SDRs não acompanham o núcleo. Davi propõe perfis; Angélica contrata conforme
escopo autorizado. A Braia chama diretamente cada agente necessário; Juliana não
compra, contrata ou cria subagentes por conta própria.
