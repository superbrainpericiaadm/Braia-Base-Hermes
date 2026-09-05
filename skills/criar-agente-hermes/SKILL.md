---
name: criar-agente-hermes
description: Formato e instalação de novos agentes e ferramentas.
version: 0.1.0
author: SuperBrain Inteligência Pericial e Contábil Ltda
license: Proprietary
metadata:
  hermes:
    category: braia-base
    tags:
    - braia
    - criar-agente-hermes
---


# Criar e integrar um adicional

Angélica usa esta skill após definir escopo e autorização. Leia
`docs/modulos.md` na raiz do perfil e copie o formato de `templates/module.yaml`.
O pacote contém `module.yaml` e `skills/<slug>/SKILL.md`; nenhum segredo ou dado de cliente.

Cada SKILL.md começa com frontmatter YAML contendo `name` igual ao diretório e
`description` específica. O corpo define identidade, quando agir, escopo, limites,
método, ferramentas reais e repasse ao chamador em RESULTADO, EVIDÊNCIA, ARQUIVOS,
BLOQUEIOS e PRÓXIMO PASSO. Instruções extensas vão a referências relativas.
Agentes adicionais são folhas. Não use prompts de outro runtime.

Crie a preparação em `workspace/preparacao-modulos/<id>` com caminhos absolutos.
Registre casos típicos e de fronteira, sem usar dados de outro cliente. A descrição
comercial do módulo deve corresponder à entrega real; licenças não são inferidas.

```bash
python /RAIZ/ABSOLUTA/DO/PERFIL/scripts/module_manager.py validate /CAMINHO/ABSOLUTO/DO/PACOTE
python /RAIZ/ABSOLUTA/DO/PERFIL/scripts/module_manager.py install /CAMINHO/ABSOLUTO/DO/PACOTE --profile /RAIZ/ABSOLUTA/DO/PERFIL
```

Após instalar, inicie nova sessão ou recarregue as skills pelo recurso disponível
no Hermes e confira `skills_list` e `skill_view` antes da primeira delegação.
Não edite o roster distribuído: o registro local complementa o núcleo e sobrevive
à atualização. O instalador recusa duplicatas; atualização de adicional nesta
versão exige pacote com novo ID/slugs ou manutenção controlada pelo instalador.
