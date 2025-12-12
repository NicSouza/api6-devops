# Documentação de Deploy

## 1. O que é Deploy <br>
Deploy (ou "deployment") é o processo de disponibilizar uma aplicação ou sistema em um ambiente específico, como produção, desenvolvimento ou testes. Essa etapa final do ciclo de desenvolvimento de software torna o código desenvolvido e testado acessível para usuários finais ou outras partes interessadas.

No projeto API 6, a estratégia de deploy adota o modelo PaaS (Platform as a Service) e GitOps, eliminando a necessidade de gerenciamento manual de servidores físicos e permitindo que atualizações no GitHub sejam refletidas nos ambientes de produção de forma ágil e segura.

## 2. Pré-requisitos <br>
- Conta ativa no GitHub com acesso ao repositório do projeto.

- Conta na plataforma Render (para o Backend).

- Conta na plataforma Vercel (para o Frontend).

- Cluster configurado no MongoDB Atlas (Database).

## 3. Configuração do Deploy e Ferramentas Utilizadas <br>
### Infraestrutura <br>
O ambiente de produção é composto por serviços em nuvem distribuídos:

### Banco de Dados: <br>

- DB: MongoDB Atlas (Cluster M0/M2), hospedado na AWS (Region: N. Virginia ou similar), acessível via Connection String segura.

### Aplicações: <br>

- Backend: Render Web Service (Python 3 environment).

- Frontend: Vercel Project (Node.js environment).

### Ferramentas <br>
- Poetry: Gerenciador de dependências utilizado para garantir que o ambiente de produção do Backend tenha as mesmas bibliotecas do desenvolvimento.

- Nx/Vite: Responsáveis pelo build otimizado e minificação dos arquivos estáticos do Frontend.

- GitHub Actions: Para a esteira de CI (Testes e Verificação).

- Integração Contínua (GitOps): Conectores nativos do Render e Vercel que observam o repositório Git.

## 4. Fluxo para Realização do Deploy <br>
### Configuração de Banco de Dados: <br>
- Criar um Cluster no MongoDB Atlas.

- Configurar a Network Access para permitir conexões do servidor do Render (0.0.0.0/0 ou lista de IPs dedicados).

- Gerar a Connection String (URI) de produção e reservar para a etapa de variáveis de ambiente.

### Configuração de Ambiente de Produção (Backend - Render):<br>
- Criar um novo Web Service no Render conectado ao repositório do GitHub.

- Definir o diretório raiz (Root Directory) como apps/api.

### Configurar os comandos de build e start:

- Build Command: poetry install <br>

- Start Command: gunicorn api.server:create_app() <br>

- Inserir as variáveis de ambiente (Environment Variables) no painel do Render, não via arquivo .env, para segurança: <br>

- MONGO_URI: <Sua string de conexão do Atlas>

- FLASK_ENV: production

### Configuração de Ambiente de Produção (Frontend - Vercel): <br>
- Importar o projeto na Vercel via GitHub.

- Definir o diretório raiz (Root Directory) como apps/web.

- A Vercel detecta automaticamente o framework (Vite) e configura o build (npm run build).

- Configurar as variáveis de ambiente no painel da Vercel:

### VITE_API_BASE_URL: <URL do Backend gerada pelo Render>

### Build e Publicação: <br>
- Diferente do modelo tradicional de Docker manual, o build é realizado na própria infraestrutura da nuvem:

- Ao receber o código, o Render cria um container efêmero, instala o Poetry, baixa as dependências e inicia o Gunicorn.

- A Vercel compila o React/TypeScript e distribui os arquivos estáticos em sua CDN global (Edge Network).

## 5. Medidas de Segurança <br>
- A exposição de credenciais e erros detalhados é um risco crítico. Para mitigar:

- Segurança de Credenciais: Jamais versionar arquivos .env ou .env.production. Todas as chaves (Tokens, URIs de Banco) são injetadas apenas em tempo de execução através dos painéis "Environment Variables" do Render e Vercel.

- Tratamento de Erros:

Definir FLASK_DEBUG=False no ambiente do Render.

Implementamos um mecanismo no Backend (conforme visto na rota de login) que intercepta erros não tratados (404/500) e retorna mensagens JSON padronizadas, evitando vazar Stack Traces do Python para o usuário final.

CORS Restrito: O Backend deve ser configurado para aceitar requisições apenas do domínio oficial do Frontend na Vercel (configurável via flask-cors), bloqueando origens desconhecidas.

## 6. Fluxo para Automatização do Deploy <br> 
- A automação segue o modelo de Entrega Contínua (Continuous Delivery), integrando o GitHub Actions com os gatilhos de deploy das plataformas.

- Integração do GitHub com as Plataformas:
Vincular a conta do GitHub ao Render e à Vercel.

- Autorizar o acesso apenas ao repositório do projeto API 6.

- Configuração do Gatilho (Trigger):
O "push" da imagem é substituído pelo "pull" do código fonte:

- Configuração: No painel do Render/Vercel, a opção Auto-Deploy deve estar habilitada para a branch main.

### O Processo: <br>

- O desenvolvedor faz o merge na main.

- O GitHub Actions roda os testes (CI).

- Se os testes passarem, o código é disponibilizado.

- O Render e a Vercel detectam o novo commit via Webhook.

- O processo de Build e Deploy inicia automaticamente.

(Nota: Para maior controle, o "Auto-Deploy" pode ser desativado nos painéis, exigindo um clique manual no botão "Deploy" após a validação da CI, caracterizando o Deploy Manual supervisionado).

## 7. Validação Pós-Deploy <br>
- Checklist de Validação
  
- Verificar se o status no painel do Render está como "Live" (Verde).

- Verificar se o deployment na Vercel está marcado como "Ready".

- Testar manualmente o fluxo crítico:

- Acessar o Frontend (URL Vercel).

- Realizar o Login (validando a conexão Front <-> Back).

- Verificar se o Token foi salvo no Storage (validando a lógica de negócio).

### Endereços de Produção: <br>
Frontend: <https://api6-devops-frontend.vercel.app>

Backend: <https://api6-devops-backend.onrender.com>
