# Braia Base

Produto-base da SuperBrain para criar equipes de IA modulares no Hermes. A base
inclui Braia, Juliana, Isaura, Paulo, Angélica e Davi; especialistas verticais e
ferramentas adicionais entram como módulos locais. A SuperBrain fornece IA,
automação e consultoria. O trabalho profissional continua sob responsabilidade
do escritório cliente.

Esta release é **v1.0.11** e usa o mesmo contrato técnico homologado da Braia
v1.0.11: escolha de modelo por tarefa, OAuth de assinatura, fallback capaz,
histórico local de entregas aceitas e prioridade conservadora entre provedores.
A proveniência exata está em [docs/proveniencia.md](docs/proveniencia.md) e as
provas desta versão estão em [docs/RELEASE-v1.0.11.md](docs/RELEASE-v1.0.11.md).

## Equipe incluída

| Agente | Responsabilidade |
|---|---|
| Braia | Conversa com o dono, escolhe a rota, coordena e valida. |
| Juliana | Executa operações e processos como especialista. |
| Isaura | Secretaria, atendimento, documentos, e-mail e agenda. |
| Paulo | Desenvolvimento, integrações, scripts e automações. |
| Angélica | Contratação, criação, treinamento e integração de agentes. |
| Davi | Processo comercial e coordenação de SDRs instalados. |

Rebeca, Rogério, SDRs especializados e outras ferramentas não acompanham o
núcleo. A base consulta `local/module-registry.json` antes de anunciar ou chamar
um adicional. Veja [docs/modulos.md](docs/modulos.md).

## Assinaturas e modelos

Uma assinatura ChatGPT/Codex ou Claude basta. A segunda é opcional. O dono
escolhe o orquestrador e a preferência inicial fica salva. Cada subagente recebe
um modelo do provedor ativo:

| Trabalho | Claude | ChatGPT/Codex |
|---|---|---|
| Rotina delimitada | Haiku | Luna |
| Trabalho normal | Sonnet | Terra |
| Trabalho complexo | Opus | Sol |
| Exceção demonstrada | Fable, se disponível | Astra, se disponível |

Com duas assinaturas, indisponibilidade pode usar a outra com capacidade
adequada. Entregas realmente validadas alimentam um histórico local para ajustar
prioridade entre tarefas comparáveis. Escolha manual prevalece; não há mudança
por uma falha isolada. Consulte [POLITICA-FALLBACK.md](POLITICA-FALLBACK.md).

Depois que a instalação já consegue conversar, Claude conecta pela conversa
privada: a Braia envia o link, o dono autoriza no site e devolve o código
completo. O fluxo usa OAuth de assinatura, sem API key, terminal para o cliente
ou ativação de uso extra. A escolha e o login da primeira assinatura em novas
instalações ficam para a etapa do Worker. Google também é opcional e continua
no fluxo `braia-google-login`.

## Requisitos homologados

- Hermes 0.21.0 na árvore Git revisada
  `59d8aa0a3099a0a74aab6f9abd2c4ffcc8ddf5d2`;
- Python 3.10 ou superior, PyYAML e Git;
- ao menos uma assinatura OAuth conectada no próprio perfil;
- runtime com `runtime-patches/delegation-fallback.patch` aplicado.

O helper recusa outra árvore do Hermes e preserva qualquer alteração local. Uma
versão mais nova do Hermes exige nova revisão do patch; o requisito semântico no
manifesto não substitui essa conferência.

## Instalação manual de referência

O Worker de novas instalações será integrado em outra etapa. Para homologação ou
suporte manual, use clones limpos na tag `v1.0.11` e caminhos absolutos. Nos
comandos abaixo, `KIT` é este repositório, `PERFIL` é a raiz efetiva do perfil,
`RUNTIME` é o clone do Hermes e `BACKUP` fica fora dele.

```bash
git clone --branch v1.0.11 --depth 1 https://github.com/superbrainpericiaadm/Braia-Base-Hermes.git "$KIT"
hermes profile install "$KIT" --name braia-base --alias -y
hermes -p braia-base auth
python "$PERFIL/scripts/profile_setup.py" --profile "$PERFIL"
python "$PERFIL/scripts/apply_runtime_patch.py" --runtime "$RUNTIME" --backup-root "$BACKUP" --check
python "$PERFIL/scripts/apply_runtime_patch.py" --runtime "$RUNTIME" --backup-root "$BACKUP"
HERMES_HOME="$PERFIL" PYTHONPATH="$RUNTIME" python "$PERFIL/scripts/configure_multi_ai.py" --check
HERMES_HOME="$PERFIL" PYTHONPATH="$RUNTIME" python "$PERFIL/scripts/configure_multi_ai.py"
hermes -p braia-base config check
```

Pare gateway e processos do runtime antes de aplicar o patch e reinicie somente
após `config check` e uma inferência real. O configurador lê apenas as contas do
perfil, recusa API key e preserva configuração, dados e módulos alheios às rotas.

Peça “execute o onboarding da Braia Base”. O setup cria workspace e namespace
local, registra governança e conserva adicionais. Para Telegram, configure o bot
exclusivo e a allowlist no `env-path`, valide o destinatário e só então instale o
gateway. Nenhuma prospecção, cron ou envio nasce ativado.

## Uma camada de delegação

A Braia consulta a prioridade do provedor, escolhe o modelo de cada subtarefa e
despacha diretamente Juliana, Davi ou outro especialista como `leaf`, com rota
explícita. A profundidade máxima é 1 e o lote admite até três especialistas.
Nenhum especialista cria outra camada. O runtime registra conclusão e
`execution_id`; a Braia só grava aceite após conferir a evidência.

## Atualização

Atualizações exigem tag fixa, backup e perfil ocioso. O núcleo distribuído pode
mudar; `local/`, `workspace/`, OAuth, memórias, sessões, bancos e personalizações
não podem ser substituídos. A migração de `0.1.0` para `1.0.11` também aplica o
runtime e roda o configurador de rotas. Veja [docs/atualizacao.md](docs/atualizacao.md).

## Desenvolvimento

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

Os testes locais validam pacote, configuração, migração e segurança do helper.
A suíte do patch roda contra a árvore exata do Hermes em ambiente Linux isolado.
Google, Telegram e inferência precisam de contas próprias do ambiente de teste.
