# crawler_yahoo_finance

Scraper de dados de equities do Yahoo Finance. Navega pelo screener de ações, aplica filtro de região e extrai símbolo, nome e preço de todas as páginas, salvando o resultado em CSV.

## Requisitos

- [Python 3.14+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/) instalado
- [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) compatível com a versão do Chrome

Ou simplesmente [Docker](https://www.docker.com/) para rodar sem instalar nada localmente.

## Instalação local

```bash
# Fedora/RHEL
sudo dnf install python3.14

# Poetry via pipx
pip install pipx
pipx install poetry
poetry config virtualenvs.in-project true

# Dependências do projeto
cd crawler_yahoo_finance
poetry install
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

| Variável      | Descrição                         | Exemplo                                                   |
|---------------|-----------------------------------|-----------------------------------------------------------|
| `LOG_LEVEL`   | Nível de log                      | `DEBUG`                                                   |
| `CONSOLE_LOG` | Habilita log no terminal          | `TRUE`                                                    |
| `LOG_FILE`    | Caminho para arquivo de log       | `./app.log` (opcional)                                    |
| `CSV_NAME`    | Prefixo do arquivo CSV            | `equities`                                                |
| `DATA_PATH`   | Diretório base de saída           | `./data` (local) ou `/data` (Docker)                      |
| `URL`         | URL do screener                   | `https://finance.yahoo.com/research-hub/screener/equity/` |
| `REGION`      | Filtro de região                  | `United States`                                           |

O CSV gerado é salvo em `<DATA_PATH>/YYYY/MM/DD/<CSV_NAME>_<timestamp_ms>.csv`.

## Como rodar

### Local

```bash
poetry run python src/main.py
```

### Docker

```bash
docker compose up
```

Os CSVs são salvos em `./data/` localmente via volume montado. Certifique-se de que `DATA_PATH=/data` no `.env`.

## Como rodar testes

```bash
poetry run pytest
```

O relatório de cobertura é exibido automaticamente no terminal (`--cov=src --cov-report=term-missing`).

### Estrutura dos testes

```
test/
├── conftest.py          # Fixtures compartilhadas
├── const_fixtures.py    # Constantes HTML para testes de parsing
├── factories.py         # EquityFactory com factory-boy e Faker
├── test_parser.py       # Testes do parser HTML
└── test_file_handler.py # Testes do handler de CSV
```

## Tecnologias usadas

### Produção

| Biblioteca        | Uso                                      |
|-------------------|------------------------------------------|
| Selenium          | Automação do browser                     |
| BeautifulSoup4    | Parsing do HTML da tabela                |
| Pydantic          | Validação e modelagem dos dados          |
| Pydantic-Settings | Carregamento de configuração via `.env`  |
| Tenacity          | Retry com backoff exponencial            |

### Desenvolvimento

| Biblioteca   | Uso                                          |
|--------------|----------------------------------------------|
| Pytest       | Testes automatizados                         |
| pytest-cov   | Relatório de cobertura de código             |
| Factory Boy  | Factories para geração de objetos nos testes |
| Faker        | Geração de dados falsos realistas            |

## Decisões técnicas

- **Selenium** — o screener do Yahoo Finance é uma SPA React que requer JavaScript para renderizar os dados, inviabilizando scraping com `requests` puro.
- **BeautifulSoup para parsing** — após capturar o HTML renderizado, o parsing é feito fora do browser para melhor performance e testabilidade.
- **Pydantic para validação** — garante que preços negativos ou dados malformados sejam rejeitados antes de chegar ao CSV.
- **Tenacity para retry** — falhas de timeout do Selenium são retentadas automaticamente com backoff exponencial (1s → 2s → 4s), com logging de cada retentativa.
- **Factory Boy + Faker nos testes** — dados gerados dinamicamente evitam hardcode e tornam os testes mais robustos contra variações de input.
- **Docker multi-stage** — stage `build` instala dependências em um `.venv` isolado; stage `run` copia apenas o venv e o `src/`, mantendo a imagem final enxuta.

## Melhorias futuras

### Coleta de dados
- **Mais campos por equity** — capturar volume, variação diária (%), market cap e setor além de símbolo, nome e preço.
- **Múltiplas regiões** — aceitar uma lista de regiões via `.env` e executar o scraper para cada uma em sequência, gerando CSVs separados ou unificados.

### Armazenamento
- **Saída em Parquet** — melhora o consumo das informacoes.


### Execução
- **Execução paralela de páginas** — coletar múltiplas páginas concorrentemente com `asyncio` + Selenium Grid ou Playwright para reduzir o tempo total de extração.

### Observabilidade
- **Métricas de execução** — registrar no log o número de equities coletadas, páginas processadas, erros de parsing e tempo total de execução.
- **Monitoramento** — acompanhar o número de falhas no processo e notificar quando a qualidade do resultado estiver abaixo do esperado.

