# Projeto ETL com API e Banco de Dados PostgreSQL

Este projeto implementa um pipeline ETL que consome dados de uma API, agrega as informações em janelas de 10 minutos, e armazena os resultados em um banco de dados PostgreSQL.

## Requisitos

- Docker
- Docker Compose


## Como rodar o projeto

### 1. Subir os containers

```bash
docker-compose up --build
```

Isso irá:

- Subir a API de origem (`api_fonte`)
- Criar automaticamente a tabela no banco de dados de destino (`db_alvo`)
- Subir o container do ETL

### 2. Executar o ETL

Para rodar o ETL manualmente:

```bash
docker-compose exec etl python etl/run_etl.py 01-01-2025 temperatura umidade
```

Substitua a data e os nomes das colunas conforme desejado. Alcance de datas no banco fonte: 01-01-2025 a 10-01-2025

## Testes manuais no banco de dados

Acesse o banco via terminal:

```bash
docker-compose exec db_alvo psql -U user -d alvo
```

Comandos úteis:

```sql
-- Ver todas as tabelas
\dt

-- Ver estrutura da tabela signal
\d signal

-- Consultar dados
SELECT * FROM signal LIMIT 10;

-- Sair do psql
\q
```

## Detalhes do ETL

- O ETL consome dados da API para um dia específico e colunas informadas via linha de comando.
- Os dados são agregados em janelas de 10 minutos com as métricas: média, mínimo, máximo e desvio padrão.
- Os nomes das colunas são combinados com o tipo de agregação, gerando campos como `ambient_temperature_mean`, `wind_speed_max`, etc.
- Cada combinação `name` recebe um `signal_id`.
- Os dados finais são inseridos na tabela `signal`.

## Estrutura da Tabela `signal`

| Campo      | Tipo                   |
|------------|------------------------|
| id         | Integer (PK, autoincrement) |
| name       | String |
| data       | Date                   |
| timestamp  | Time                   |
| signal_id  | Integer                |
| value      | Float                  |

## Observações

- Os dados existentes no banco não são apagados ao rodar o ETL novamente.
- Para reiniciar do zero, utilize:

```bash
docker-compose down -v
```

Isso derruba os containers e remove os volumes, apagando os dados persistidos. 
