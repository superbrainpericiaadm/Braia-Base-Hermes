# Núcleo e adicionais

Braia Base é a fonte comum, versionada independentemente das verticais. Rebeca
(perícia judicial) e Rogério (tributário) são adicionais previstos. Este repositório
não os empacota, não os libera e não define preço. Ferramentas e futuros agentes
usam o mesmo formato de pacote, sem exigir copiar a distribuição inteira.

## Formato de pacote

Um diretório local, obtido de fonte autorizada, contém `module.yaml` e
`skills/<slug>/SKILL.md`, com referências/scripts auxiliares dentro de cada skill.
Veja `templates/module.yaml`. `kind` pode ser `agent` ou `tool`.
Ferramentas usam `agents: []`; sua skill orienta a integração. Dependências externas
e credenciais são configuradas separadamente, sem execução automática de instaladores.
`base_requires` aceita intervalos semver numéricos separados por vírgula. Para
esta release, use `>=1.0.11,<2.0.0` quando o módulo depender do roteamento novo.

```bash
python /PERFIL/scripts/module_manager.py validate /PACOTE
python /PERFIL/scripts/module_manager.py install /PACOTE --profile /PERFIL
python /PERFIL/scripts/module_manager.py list --profile /PERFIL
```

Todos os caminhos acima devem ser substituídos por caminhos absolutos reais.
O instalador valida manifesto, compatibilidade, frontmatter, nomes e colisões;
recusa links simbólicos e não executa scripts do pacote. Ele copia as skills para
`local/skills/` e registra agentes em `local/module-registry.json`.
Esses caminhos são preservados pelo update do Hermes. Em uma nova sessão, a Braia
consulta o registro e confirma a skill disponível antes de delegar.

Instalação exige autorização e origem confiável. Validação estrutural não equivale
a auditoria de código nem licença comercial. Esta versão não implementa cobrança,
assinatura criptográfica ou DRM. Não há remoção/update automático de módulos:
manutenção exige backup e revisão pelo instalador, preservando dados e registro.

## Responsabilidades

- Braia valida necessidade e entrega ao cliente.
- Angélica cria/contrata e integra o agente ou módulo autorizado.
- Paulo implementa integrações técnicas.
- Juliana instancia agentes existentes para executar operações.
- Davi gerencia SDRs contratados, sem assumir que eles já vêm no pacote.

Alterações do núcleo vão a este repositório; personalizações não editam suas skills.
Os módulos não devem sobrescrever identidades nem dependências do núcleo.
