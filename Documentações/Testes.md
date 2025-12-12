# Documentação de Testes de Integração ou Unitários <br>

## 1. O que são nossos testes? <br>
São testes projetados para validar a lógica de negócios e a interação entre a camada de serviço e a camada de dados. No projeto Khali API 6, eles garantem que o cálculo de safras (Yield Model), a manipulação de dados e as regras de inserção no MongoDB estão funcionando como esperado.

Diferente de testes que sobem containers pesados (o que tornaria a CI lenta), adotamos uma estratégia de Testes Isolados com Mocks. Isso verifica cenários reais de uso — como criar um evento de safra ou filtrar dados — simulando o banco de dados em memória. Isso é essencial para assegurar que os módulos estejam corretos antes de enviarmos o código para o ambiente de produção (Render).

## 2. Estrutura dos Testes <br>
Os testes no projeto estão organizados dentro do diretório tests na raiz da aplicação (apps/api). Eles utilizam o framework Pytest e bibliotecas padrão da indústria Python:

- pytest: O runner principal para execução e descoberta dos testes.

- unittest.mock (MagicMock): Para simular o comportamento do banco de dados MongoDB, permitindo testar o sucesso e falhas de conexão sem precisar de um banco real rodando.

- mongomock: Uma biblioteca auxiliar que simula a estrutura de documentos do Mongo em memória.

### Cada teste segue um fluxo comum: <br>

- Arrange (Configuração): Inicialização dos Fixtures (dados falsos e conexão simulada).

- Act (Ação): Execução da função de negócio (ex: create_yield_event).

- Assert (Validação): Verificação se o método de "salvar" foi chamado corretamente e se os dados retornados estão no formato esperado.

## 2.1. Configuração de Ambiente <br>
Para evitar repetição de código e garantir isolamento, utilizamos o recurso de Fixtures do Pytest. Em vez de criar um IntegrationEnvironment complexo, nós injetamos dependências controladas.

O arquivo de testes configura automaticamente o ambiente antes de cada função rodar:

### Exemplo de Fixture (mock_mongo): <br>

```Python

@pytest.fixture
def mock_mongo():
    client = MongoClient()
    db = client['test_db']
    yield db 

```

### Exemplo de Patch (Intercepção): <br>

```Python
@pytest.fixture(autouse=True)
def patch_connect(mock_mongo):
    with patch.object(MongoDB, "connect", return_value=mock_mongo):
        yield

```

### O ambiente padrão inclui: <br>

- Mock do Cliente Mongo: Garante que nenhum dado seja gravado no Atlas (Produção) durante os testes.

- Dados de Exemplo (sample_event): Um dicionário pronto com dados de uma safra (Trigo, 2024, California) para padronizar os testes.

## 3. Como executar os testes <br>
O projeto utiliza o gerenciador de dependências Poetry para garantir que os testes rodem em um ambiente isolado e controlado.

### Comando principal <br>
O comando abaixo executa a bateria completa de testes do Backend, gerando um relatório visual no terminal:

```Bash

poetry run pytest

```
Este comando irá:

- Verificar o arquivo pytest.ini para configurações.

- Localizar todos os arquivos que começam com test_ dentro de apps/api.

- Executar as funções de teste e exibir ✅ (Passou) ou ❌ (Falhou).

### Execução de um arquivo específico: <br>
Para validar apenas um módulo (útil durante o desenvolvimento), você pode apontar o arquivo:

```Bash

poetry run pytest tests/test_yield_unit.py

```

## 4. Convenções e Boas Práticas
### 4.1 Estrutura dos testes
Os testes seguem uma estrutura previsível para facilitar a manutenção:

- Mockagem Explicita: Cada teste deve definir o que espera do banco de dados.

- Exemplo: "Vou testar a busca. Então, finja que o banco retornou uma lista com 1 item".

- Código: yield_collection.find = MagicMock(return_value=[sample_event]).

- Asserções de Chamada: Não verificamos apenas o resultado, verificamos se o banco foi chamado.

- Código: yield_collection.insert_one.assert_called_once().

### 4.2 Configuração de ambiente
Antes de rodar os testes, certifique-se de que:

- O Poetry está instalado e as dependências foram baixadas (poetry install).

- Você está na pasta correta (apps/api).

### 4.3 Organização dos arquivos
Os testes estão localizados estrategicamente:

- apps/api/tests/: Contém os testes unitários e de integração simulada das regras de negócio (Yield Model).

## 5. Exemplos de Casos de Testes <br> 

### 5.1 Teste de Criação (Create) <br>

- Objetivo: Garantir que o sistema consegue receber um objeto de safra e enviar para o banco.

Fluxo: 

- Recebe o sample_event (dados da safra).

- Simula que o banco respondeu com um ID de sucesso ("123").

- Chama create_yield_event.

- Valida se o ID retornado não é nulo.

### 5.2 Teste de Leitura com Filtro (Read) <br>
- Objetivo: Garantir que a função de busca retorna os dados formatados corretamente.

Fluxo:

- Configura o Mock para retornar uma lista fixa.

- Chama get_yield_events_filter.

- Valida se a lista retornada é idêntica à lista injetada no Mock.

### 5.3 Teste de Atualização (Update) <br>
- Objetivo: Garantir que a atualização de uma safra (ex: mudar produção de 5000 para 6000) respeite os critérios.

Fluxo:

- Configura o Mock para dizer "1 documento foi modificado".

- Altera um valor no dicionário de dados.

- Chama update_yield_event.

- Valida se modified_count é igual a 1.

## 6. Resolução de Problemas comuns <br>
- ModuleNotFoundError: Geralmente ocorre se você tentar rodar o pytest fora do ambiente virtual.

- Solução: Sempre use poetry run pytest.

- NotImplementedError (Mongomock): Ocorre se tentarmos usar recursos avançados do Mongo (como Schema Validation) no banco de memória.

Solução: Nossos testes utilizam mocks simplificados (MagicMock) para evitar essa complexidade e focar na regra de negócio.

Testes não encontrados: Verifique se você está na pasta apps/api. O pytest procura os arquivos a partir do diretório atual.
