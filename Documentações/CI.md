### Configuração de CI <br>

## 1. O que é CI? <br>
Continuous Integration (CI) é uma prática de desenvolvimento que automatiza a integração de código de diferentes desenvolvedores em um único repositório. O objetivo é detectar erros rapidamente, garantindo que o código seja testado e validado antes de ser integrado ao projeto principal.

No projeto API 6, utilizamos o GitHub Actions como ferramenta de CI. As pipelines estão definidas em arquivos YAML localizados na pasta .github/workflows do repositório, gerenciando tanto o Back-end (Python) quanto o Front-end (React).

## 2. Configuração da CI <br>
No projeto, configuramos três pipelines principais para garantir a qualidade e a entrega:

- Build & Check Pipeline: Responsável por instalar as dependências e verificar se o código compila corretamente (Front-end e Back-end), garantindo que não há erros de sintaxe que impeçam a execução.

- Unit Tests (Back-end): Executa os testes unitários automatizados utilizando pytest e poetry. Esta etapa valida as regras de negócio críticas (como o cálculo de safra) e a integridade dos Models antes de aceitar o código.

- Deploy Automatizado: Automatiza o envio do projeto para os ambientes de produção (Render para a API e Vercel para a Web) assim que o código é aprovado.

## 3. Gatilhos e Rotina de CI <br>

### 3.1 Gatilhos das pipelines de testes e build <br>

As pipelines de verificação (Build e Testes Unitários do Back-end) são disparadas nos seguintes cenários:

- Push: Para qualquer branch de feature ou correção.

- Pull Request: Sempre que um desenvolvedor tenta enviar código para a branch main.

Isso serve como um "Portão de Qualidade" (Quality Gate). O GitHub bloqueia o merge caso os testes do Back-end falhem ou o build do Front-end quebre.

### 3.2 Gatilhos das pipelines de deploy <br>
O processo de deploy segue o modelo GitOps e é acionado automaticamente em:

- Push na branch main: Assim que um Pull Request é aprovado e mergeado na branch principal, o deploy é disparado.

- Front-end: A Vercel detecta a alteração na main e publica a nova versão.

- Back-end: O Render detecta o novo commit, baixa as dependências e reinicia o serviço.

## 4. Como contribuir com a CI <br>
Para trabalhar de forma integrada ao pipeline de CI do projeto API 6, siga estas etapas:

- Commit regularmente em sua branch de trabalho para evitar conflitos grandes.

- Antes de abrir um Pull Request, verifique se os testes do back-end estão passando localmente rodando o comando: poetry run pytest (na pasta apps/api).

- Aguarde a finalização das Actions no GitHub. Se aparecer um "X" vermelho, verifique o log, corrija o erro e suba o código novamente.
