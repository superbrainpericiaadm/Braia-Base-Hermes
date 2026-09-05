---
name: braia-google-login
description: "Conecta a conta Google do dono com o cliente OAuth da Braia."
version: 1.1.0
author: "SuperBrain Inteligência Pericial e Contábil Ltda"
license: "Proprietary"
metadata:
  hermes:
    tags: [braia, google, gmail, agenda, drive, docs, sheets, oauth, login, conectar]
    category: braia-base
    requires_toolsets: [file, terminal, skills]
---

# Login no Google

## Quando usar

Use sempre que o Chefe pedir para conectar, autorizar, logar ou vincular a conta Google, ou quando uma tarefa de Gmail, Agenda, Drive, Docs ou Sheets falhar por falta de autenticação. Frases típicas: "faz login no Google", "conecta meu Gmail", "autoriza minha agenda", "libera o Drive", "quero vincular minha conta Google".

Esta skill tem precedência sobre o roteiro de primeira configuração da skill bundled `google-workspace`. O passo "criar credenciais no Google Cloud Console" daquele roteiro **não se aplica** à Braia: o cliente OAuth do app da Braia deve ser provisionado localmente pelo instalador SuperBrain antes deste fluxo. E o Chefe **não copia nada**: ele abre a URL, autoriza, vê "Google conectado" e volta para a conversa.

## O que já existe no perfil

- `${HERMES_HOME}/google_client_secret.json`: cliente OAuth do app da Braia, do tipo aplicativo da Web, com retorno no portal da SuperBrain. É provisionado pelo instalador SuperBrain fora do Git; não acompanha a distribuição base. Nunca peça esse arquivo ao Chefe, nunca peça client ID ou chave, nunca mande criar projeto ou ativar APIs no Google Cloud.
- `${HERMES_HOME}/google_token.json`: nasce quando o Chefe autoriza. É o único arquivo gerado por instalação. Se existir e `--check` responder `AUTHENTICATED`, a conta já está conectada: não repita o login.
- `${HERMES_HOME}/skills/braia-google-login/scripts/google_login.py`: gera a URL e conclui a conexão sozinho, em segundo plano, assim que o Chefe autoriza.
- Os scripts bundled ficam em `${HERMES_HOME}/skills/productivity/google-workspace/scripts/`. Com o perfil ativo, `HERMES_HOME` é a raiz do perfil.

## Procedimento

Defina os atalhos e siga a ordem. Cada passo é um comando de `terminal`.

```bash
GSETUP="python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py"
GLOGIN="python ${HERMES_HOME}/skills/braia-google-login/scripts/google_login.py"
$GSETUP --check
```

1. Se `--check` responder `AUTHENTICATED`, avise o Chefe que a conta já está conectada e pare.
2. Confira que `${HERMES_HOME}/google_client_secret.json` existe. Se não existir, o provisionamento Google ainda não foi concluído: avise o Chefe e peça suporte à SuperBrain. Não tente criar o arquivo.
3. Registre o cliente e gere a URL:

```bash
$GSETUP --install-deps
$GSETUP --client-secret ${HERMES_HOME}/google_client_secret.json
$GLOGIN start
```

4. Envie ao Chefe, **somente na DM**, a URL impressa. Explique em uma frase: abrir no computador ou celular, entrar com a conta Google do escritório e aceitar os acessos. Diga que, ao aparecer "Google conectado", é só voltar aqui e avisar. Não peça código, link ou print.
5. Quando o Chefe avisar (ou depois de alguns minutos), confira:

```bash
$GLOGIN status
$GSETUP --check
```

   `AUTENTICADO` mais `AUTHENTICATED`: conectado. `PENDENTE`: o Chefe ainda não autorizou; espere e confira de novo, sem gerar outra URL. `ERRO`: leia o motivo, explique ao Chefe e, se fizer sentido, rode `$GLOGIN start` de novo para uma URL nova.
6. Com `AUTHENTICATED`, confirme ao Chefe que Gmail, Agenda, Drive, Docs e Sheets estão conectados e volte à tarefa que ele pediu. Use `--check-live` se quiser provar com uma chamada real.

## Erros conhecidos

- `ERRO access_denied` ou `Error 403: access_denied` na tela do Google: o app da Braia está em fase de teste no Google e o e-mail do Chefe ainda não foi liberado. Avise o Chefe que a SuperBrain precisa cadastrar o e-mail dele como usuário de teste do app e peça que ele acione o suporte. Não tente contornar criando outro cliente.
- `ERRO o dono não autorizou em 15 minutos`: a URL venceu. Gere outra com `$GLOGIN start` e reenvie na DM.
- `ERRO troca do código falhou`: a URL foi usada duas vezes ou venceu. Gere outra com `$GLOGIN start`.
- Se o Chefe colar por conta própria uma URL de retorno na DM, ainda funciona: passe-a inteira a `$GSETUP --auth-code "<url>"` e confira com `--check`. Se ele colar num grupo, descarte: gere URL nova e oriente a usar a DM.
- Opções `--services` e `--format` aparecem no roteiro bundled, mas o `setup.py` desta versão não as aceita. Não as use.

## Regras

- Não peça, não copie e não cole em chat o conteúdo de `google_client_secret.json` ou de `google_token.json`.
- Não mande o Chefe criar projeto, ativar APIs ou baixar JSON no Google Cloud Console. Isso só valeria se a SuperBrain descontinuasse o app da Braia, e nesse caso a distribuição traria um arquivo novo.
- Não use `$GSETUP --auth-url`: ele aponta o retorno para `localhost` e obriga o Chefe a copiar link. O caminho da Braia é `$GLOGIN start`.
- Leitura e pesquisa são livres depois de conectado; rotulagem altera dados e exige autorização compatível. Enviar e-mail, criar ou apagar evento, compartilhar ou apagar arquivo e alterar Docs ou Sheets continuam exigindo pedido ou autorização explícita do Chefe, como em [Limites](../../SOUL.md).
