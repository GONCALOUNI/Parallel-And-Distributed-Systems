# KVerse

**KVerse** é uma solução distribuída leve para armazenamento key-value, desenvolvida com FastAPI, SQLite e Docker Compose. Proporciona uma API REST simples para armazenar, recuperar e eliminar pares chave-valor arbitrários, com uma configuração mínima e uma ênfase na facilidade de utilização.

---

## Índice

* [Funcionalidades](#funcionalidades)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Pré-requisitos](#pré-requisitos)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Instalação](#instalação)
* [Execução da Aplicação](#execução-da-aplicação)
* [Documentação da API](#documentação-da-api)
* [Exemplos de Utilização](#exemplos-de-utilização)
* [Execução de Testes](#execução-de-testes)
* [Licença](#licença)

---

## Funcionalidades

* **API RESTful** para operações PUT, GET, DELETE
* Endpoint para **verificação de saúde (health check)**
* Persistência com **SQLite** (criação automática do diretório de dados)
* Orquestração com **Docker Compose** para inicialização com um único comando
* Documentação **OpenAPI** gerada automaticamente através do FastAPI
* **Testes unitários** com pytest

---

## Tecnologias Utilizadas

* **Backend**: FastAPI (Python 3.11)
* **Base de Dados**: SQLite (baseada em ficheiros)
* **Contentorização**: Docker & Docker Compose
* **Testes**: pytest, TestClient

---

## Pré-requisitos

* Docker Engine
* Docker Compose (ou utilizar o plugin `docker compose`)
* Git

---

## Estrutura do Projeto

```
KVerse/
├── backend/               # Serviço e código da API
│   ├── .venv/             # Ambiente virtual Python (ignorado pelo git)
│   ├── main.py            # Aplicação FastAPI
│   ├── requirements.txt   # Dependências Python
│   ├── Dockerfile         # Instruções de construção do contentor
│   └── tests/             # Testes unitários (pytest)
├── data/                  # Diretório de dados SQLite (ignorado pelo git)
├── docs/                  # Documentação, diagramas, etc.
│   └── arquitetura.drawio
├── docker-compose.yml     # Orquestração do Docker Compose
├── start.sh               # Script de inicialização (executável)
├── LICENSE                # The Unlicense
└── README.md              # Este ficheiro
```

---

## Instalação

1. **Clonar o repositório**

   ```bash
   git clone git@github.com:<seu-utilizador>/KVerse.git
   cd KVerse
   ```

2. **Opcional (desenvolvimento local)**: criar um ambiente virtual Python para o backend

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   cd ..
   ```

3. **Inicializar com Docker Compose**

   ```bash
   ./start.sh
   ```

Isto irá construir e iniciar o serviço da API na porta **8000**, persistindo os dados em `./data/db.sqlite`.

---

## Execução da Aplicação

* Aceder à API em: `http://localhost:8000`
* Abrir a documentação interativa em: `http://localhost:8000/docs`

---

## Documentação da API

O FastAPI gera automaticamente documentação. Visite `/docs` (Swagger UI) ou `/redoc` (ReDoc).

---

## Exemplos de Utilização

```bash
# Verificação de saúde
curl http://localhost:8000/health

# Armazenar um valor
curl -X PUT http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"data":{"key":"foo","value":"bar"}}'

# Recuperar um valor
curl http://localhost:8000/?key=foo

# Eliminar um valor
curl -X DELETE http://localhost:8000/?key=foo
```

---

## Execução de Testes

A partir da raiz do projeto ou dentro de `backend/`:

```bash
# Se estiver dentro de backend:
cd backend
python -m pytest -q
```

Todos os testes devem passar, o que valida o endpoint de verificação de saúde e as operações CRUD.

---

## Licença

Este projeto é libertado para o domínio público sob a licença **The Unlicense**. Consulte o ficheiro [LICENSE](LICENSE) para mais detalhes.
