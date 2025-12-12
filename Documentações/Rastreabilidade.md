# Documentação de Rastreabilidade e Gestão de Mudanças

## 1. O que é Rastreabilidade em DevOps?

A **Rastreabilidade** é a capacidade de acompanhar o ciclo de vida de uma funcionalidade ou correção de software desde sua concepção (requisito de negócio) até sua implementação (código) e entrega (deploy).

No projeto **Khali (API 6)**, a rastreabilidade não é apenas um registro passivo, mas um processo ativo integrado à plataforma GitHub. Isso garante que cada linha de código alterada possa ser justificada por uma demanda específica, facilitando auditorias, *rollbacks* e o entendimento do histórico do projeto.

## 2. Ferramentas e Estratégia

Centralizamos todo o gerenciamento de ciclo de vida da aplicação (ALM) no ecossistema **GitHub**, eliminando a necessidade de ferramentas externas e reduzindo a fragmentação da informação.

### Componentes Utilizados

* **GitHub Projects (Kanban):** Para gestão visual do fluxo de trabalho e priorização (Backlog, To Do, In Progress, Done).
* **Issues:** Representam a "Verdade Única" do requisito. Cada tarefa técnica ou história de usuário nasce como uma Issue.
* **Branches:** Utilizadas para isolar o desenvolvimento de novas funcionalidades.
* **Pull Requests (PR):** O ponto de convergência onde o código é revisado e vinculado à Issue original.
* **Commits Semânticos:** Histórico granular das alterações no código.

## 3. Fluxo de Rastreabilidade

O fluxo de trabalho foi desenhado para criar vínculos automáticos (links) entre as etapas do desenvolvimento:

### 3.1. Planejamento (A Issue)

Nenhuma linha de código é escrita sem uma **Issue** correspondente.

* A Issue define **"O Quê"** precisa ser feito e **"Por Quê"**.
* Exemplo real do projeto: **Issue #75** - *Implementar o botão de logout*. Nela, foram definidos os critérios de aceite (ex: remover token do localStorage).

### 3.2. Desenvolvimento (A Branch)

O desenvolvedor cria uma branch específica para aquela tarefa. Isso isola o código da versão estável (`main`).

* Padrão de nomenclatura: `feat/logout-button` ou `fix/login-error`.

### 3.3. Integração (O Pull Request)

Esta é a etapa crítica da rastreabilidade. Ao abrir um **Pull Request (PR)**, utilizamos palavras-chave especiais ("Magic Words") do GitHub para vincular o código à tarefa.

* **Automação de Fechamento:** Ao utilizar termos como `closes #75`, `fixes #75` ou `resolve #75` na descrição do PR, o GitHub cria um vínculo rígido.
* **Efeito:** Assim que o PR é aprovado e mergeado, a Issue original é movida automaticamente para "Done" e fechada. Isso garante que o status do projeto (Kanban) esteja sempre sincronizado com o código real.

### 3.4. Implementação (O Commit)

Os commits seguem padrões que facilitam a leitura do histórico. O GitHub indexa esses commits dentro da página do PR, permitindo que um auditor veja exatamente quais arquivos foram modificados para atender àquela demanda específica.

## 4. Estudo de Caso Real (Evidência de Rastreabilidade)

Para demonstrar a eficácia do processo, destacamos o fluxo de implementação da funcionalidade de Logout:

1. **Origem:** Criação da **Issue #75** detalhando a necessidade de segurança no encerramento de sessão.
2. **Desenvolvimento:** O código foi desenvolvido em branch separada e enviado via **Pull Request #94**.
3. **Vínculo:** Na descrição do PR #94, foi inserida a tag `resolve Implentar o botão de logout #75`.
4. **Conclusão:** O merge do PR disparou o fechamento automático da Issue e registrou o **Commit 857595b** como a solução definitiva.

Este fluxo comprova que o código em produção (Deploy) é resultado direto de uma tarefa planejada e aprovada.

## 5. Benefícios da Abordagem

A adoção deste modelo rigoroso de rastreabilidade trouxe os seguintes benefícios para a equipe de DevOps:

* **Auditoria Simplificada:** É possível responder rapidamente "Quem alterou isso e por quê?" apenas clicando no histórico ("Blame") de qualquer arquivo.
* **Contexto Técnico:** Novos desenvolvedores conseguem entender decisões passadas lendo a discussão na Issue vinculada ao código.
* **Automação de Status:** Elimina o erro humano de "esquecer de mover o card" no Kanban, já que o código comanda o status da tarefa.
