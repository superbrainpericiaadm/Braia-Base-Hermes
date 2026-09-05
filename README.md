# Braia Base

Produto de entrada da SuperBrain: uma equipe de IA configurada como distribuição
de perfis do Hermes Agent. Este repositório é a fonte de evolução do núcleo comum.
A SuperBrain vende IA, automações e consultoria; quem presta serviços técnicos é o
escritório cliente, sob sua própria responsabilidade profissional.

Versão inicial **0.1.0, em desenvolvimento**. Derivada de uma fotografia do
[Braia Perícias Hermes](https://github.com/superbrainpericiaadm/Braia-esc-pericias-Hermes),
sem alterar aquele repositório. A origem exata está em [proveniência](docs/proveniencia.md).

## Equipe incluída

| Agente | Responsabilidade |
|---|---|
| Braia | Orquestradora, conversa com o cliente, direciona e valida entregas. |
| Juliana | Executora operacional, decompõe, executa rotinas e sobe subagentes. |
| Isaura | Secretaria, atendimento, documentos, e-mail e agenda. |
| Paulo | Desenvolvimento, integrações, scripts e automações. |
| Angélica | Contratação, criação, treinamento e integração de agentes. |
| Davi | Gerente dos SDRs: processo comercial, qualificação e acompanhamento. |

Rebeca (perícia judicial), Rogério (tributário), outros especialistas e ferramentas
são adicionais. Seus conteúdos não acompanham a base. Davi vem incluído; uma equipe
de SDRs especializados é contratada/configurada conforme a necessidade do cliente.
Veja o [contrato de módulos](docs/modulos.md).

## Instalação

Requer Hermes **0.20.4+**, Python **3.10+**, PyYAML e Git autenticado neste repositório
privado. A delegação requer suporte a `role="orchestrator"`; a validação dessa
capacidade faz parte da [homologação](docs/homologacao.md).

```bash
hermes profile install https://github.com/superbrainpericiaadm/Braia-Base-Hermes --name braia-base --alias -y
hermes -p braia-base config path
hermes -p braia-base auth
```

Use o diretório pai do caminho retornado por `config path` como raiz absoluta do perfil:

```bash
python /CAMINHO/ABSOLUTO/DO/PERFIL/scripts/profile_setup.py --profile /CAMINHO/ABSOLUTO/DO/PERFIL
hermes -p braia-base chat
```

Peça “execute o onboarding da Braia Base”. O script ajusta `terminal.cwd`, cria o
workspace, registra a governança e prepara o espaço preservado dos adicionais.
O modelo/provedor inicial é herdado da distribuição de origem e pode ser alterado
no `config.yaml` conforme a conta do cliente. Credenciais são sempre locais.

Google é opcional. O instalador SuperBrain provisiona o cliente OAuth fora do Git;
a skill `braia-google-login` conduz a conexão após esse provisionamento.
Sem Google conectado, arquivos locais e rotinas internas continuam disponíveis.

Para Telegram, preencha as variáveis no caminho retornado por
`hermes -p braia-base config env-path`, confira os IDs autorizados e então execute:

```bash
hermes -p braia-base gateway install
hermes -p braia-base gateway start
```

Nenhuma rotina de envio ou prospecção nasce ativada. Integrações precisam ser
configuradas e testadas no ambiente do cliente.

## Evolução

Atualizações do núcleo são feitas neste repositório. Módulos e dados de cada cliente
ficam em `local/` e `workspace/`. A distribuição usa `distribution_owned` explícito
e não distribui cron, tokens, clientes OAuth ou bases de clientes.
Consulte [atualização e rollback](docs/atualizacao.md) antes de atualizar.

```bash
hermes profile update braia-base
python /CAMINHO/ABSOLUTO/DO/PERFIL/scripts/profile_setup.py --profile /CAMINHO/ABSOLUTO/DO/PERFIL
```

## Desenvolvimento

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

O pacote configura o runtime Hermes; não inclui um runtime próprio. Testes locais
validam instalação auxiliar, módulos e preservação de dados. Conversas reais,
Google e Telegram exigem a homologação descrita na documentação.
