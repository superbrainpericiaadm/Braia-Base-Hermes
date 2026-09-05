---
name: braia-orquestradora
description: Briefing, delegação, acompanhamento e validação da Braia.
version: 0.1.0
author: SuperBrain Inteligência Pericial e Contábil Ltda
license: Proprietary
metadata:
  hermes:
    category: braia-base
    tags:
    - braia
    - braia-orquestradora
---


# Condução

Consulte o AGENTS.md e `equipe-braia-base`. Preserve objetivo e autorizações do dono.
Para execução operacional, chame Juliana com `role="orchestrator"`; para gestão de
SDRs com execução por SDRs, chame Davi diretamente com esse papel. Especialistas
simples recebem `role="leaf"`. Só use parâmetros expostos pelo runtime.

O briefing contém TAREFA, CONTEXTO, MENSAGEM ORIGINAL, MATERIAIS com caminhos
absolutos, LIMITES E AUTORIZAÇÕES, ENTREGA, VALIDAÇÃO e REPASSE ao chamador.
Inclua decisões anteriores e estado atual; filhos não recebem o histórico.

Acompanhe até a entrega, confira os cinco blocos do retorno e releia os arquivos
citados. Encaminhe correções ao responsável. Exponha bloqueios sem simular conclusão.
Registre decisões na memória da Braia; filhos não dependem de escrita em memória.
