# KVerse

[![Backend Tests](https://img.shields.io/github/actions/workflow/status/your-org/Parallel-And-Distributed-Systems/ci.yaml?branch=main&label=backend)](#ci)  
[![Frontend Tests](https://img.shields.io/github/actions/workflow/status/your-org/Parallel-And-Distributed-Systems/ci.yaml?job=frontend&branch=main&label=frontend)](#ci)  
[![Coverage](https://img.shields.io/codecov/c/gh/your-org/Parallel-And-Distributed-Systems?flag=backend&flag=frontend)](#coverage)  
[![OpenAPI Spec](https://img.shields.io/github/actions/workflow/status/your-org/Parallel-And-Distributed-Systems/gen_openapi.yaml?branch=main&label=openapi)](#openapi)

**KVerse** é uma solução distribuída de alta performance para armazenamento e recuperação de pares _key–value_.  
Desenvolvida com FastAPI (Python) no backend, Vue 3/Vite no frontend, Redis como cache e PostgreSQL/SQLite para persistência.  
Toda a orquestração de containers é feita via Docker Compose.

Este repositório inclui:

- Implementação da API REST com endpoints para inserir, consultar e remover dados.
- SPA para gerenciamento de pares _key–value_.
- Monitorização (Prometheus & Grafana).
- Testes unitários (pytest, vitest) e de carga (k6).
- Pipelines CI/CD (GitHub Actions).
- Scripts de inicialização e de integração com AWS (exemplo).

---

## 🗂 Índice

1. [Visão Geral](#visão-geral)  
2. [Tecnologias](#tecnologias)  
3. [Arquitetura](#arquitetura)  
4. [Estrutura do Repositório](#estrutura-do-repositório)  
5. [Pré-requisitos](#pré-requisitos)  
6. [Permissões Docker](#permissões-docker)  
7. [Variáveis de Ambiente](#variáveis-de-ambiente)  
8. [Desenvolvimento Local](#desenvolvimento-local)  
9. [Docker Compose](#docker-compose)  
10. [Deploy na AWS (exemplo)](#deploy-na-aws-exemplo)  
11. [Acessos Padrão](#acessos-padrão)  
12. [Monitorização](#monitorização)  
13. [Testes](#testes)  
14. [CI/CD](#cicd)  
15. [Contribuir](#contribuir)  
16. [Licença](#licença)

---

## Visão Geral

KVerse oferece:

- CRUD RESTful:  
  • `PUT /kv` insere ou atualiza  
  • `GET /kv?key=` retorna valor  
  • `DELETE /kv?key=` remove entrada  
- Health-check: `GET /health`  
- Cache em Redis para alta taxa de acessos  
- Banco de dados PostgreSQL em produção; SQLite em desenvolvimento  
- Interface web SPA (Vue 3 + Vite), otimizada para **navegadores desktop Chromium**  
- Proxy reverso Nginx com balanceamento de carga (round-robin entre duas instâncias FastAPI)  
- Métricas exportadas para Prometheus e dashboards em Grafana  

---

## Tecnologias

| Camada      | Ferramenta / Biblioteca                  |
| ----------- | ---------------------------------------- |
| Backend     | FastAPI, Uvicorn, SQLAlchemy, Databases |
| Cache / DB  | Redis, PostgreSQL (prod) / SQLite (dev) |
| Frontend    | Vue 3, Vite, Bootstrap 5                |
| Proxy       | Nginx                                    |
| Monitoração | Prometheus, Grafana                      |
| Carga       | k6                                       |
| CI/CD       | GitHub Actions                           |
| Containers  | Docker, Docker Compose                   |

---

## Arquitetura

```text
                 ┌────────────┐
                 │  Cliente   │ ← Navegador Chromium (desktop)
                 └──────┬─────┘
                        │ HTTP/SPA
                        v
               ┌────────┴────────┐
               │      Nginx      │ ← Reverse-proxy & SSL/TLS
               └──────┬───┬──────┘
                      │   │
         ┌────────────┘   └────────────┐
         │                               │
         v                               v
┌────────┴───────┐               ┌────────┴───────┐
│  backend1      │               │  backend2      │
│  (FastAPI)     │               │  (FastAPI)     │
└────────┬───────┘               └────────┬───────┘
         │                               │
    ┌────┴─────┐                   ┌─────┴─────┐
    │  Redis   │ ← Cache em memória│ PostgreSQL│ ← Persistência (produção)
    └────┬─────┘                   └───────────┘
         │
    ┌────┴─────┐
    │  SQLite  │ ← Persistência (desenvolvimento)
    └──────────┘
```

---

## Estrutura do Repositório

```text
KVerse/
├── backend/            # Serviço FastAPI
├── frontend/           # SPA Vue 3 + Vite
├── docs/               # OpenAPI, diagramas, scripts AWS
├── monitoring/         # Configuração Prometheus
├── nginx.conf          # Config Nginx
├── docker-compose.yml  # Orquestração (dev)
├── start.sh            # Inicialização Linux/macOS
├── stop.sh             # Paragem Linux/macOS
├── start.bat / stop.bat# Equivalentes Windows
└── README.md           # Este documento
```

---

## Pré-requisitos

- Docker ≥ 20.x & Docker Compose  
- Node.js ≥ 16 + npm (frontend)  
- Python 3.11 (backend)  
- Lubuntu 25.05 “Plucky Puffin” (testado)  

---

## Permissões Docker

```bash
sudo groupadd docker       # cria grupo se não existir
sudo usermod -aG docker $USER
newgrp docker              # aplica sem logout
```

---

## Variáveis de Ambiente

### Backend (`.env` ou CI)

```bash
DATABASE_URL=postgresql://user:password@postgres:5432/appdb
REDIS_URL=redis://redis:6379/0
```

### Frontend (`.env.development`)

```bash
VITE_API_URL=http://localhost:8002
```

---

## Desenvolvimento Local

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm ci
npm run dev -- --host 0.0.0.0
```

---

## Docker Compose

```bash
./start.sh    # inicia todos os serviços
./stop.sh     # para e remove volumes
```

---

## Deploy na AWS (exemplo)

> **Atenção**: instruções genéricas de exemplo, ajuste conforme sua infra.

1. Configure suas credenciais AWS:
   ```bash
   aws configure
   ```
2. Empacote a aplicação:
   ```bash
   docker compose -f docker-compose.yml pull
   docker compose -f docker-compose.yml build
   ```
3. Faça login no ECR e envie as imagens:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   docker tag backend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/kverse-backend:latest
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/kverse-backend:latest
   # repita para frontend, redis, nginx etc.
   ```
4. Use ECS / EKS / CloudFormation para orquestrar serviços no AWS.  
5. Atualize o `docker-compose.aws.yml` (ou use terraform/CloudFormation) para apontar às imagens no ECR.  
6. Disponibilize o endpoint via Elastic Load Balancer (ELB) e configure certificados ACM.

---

## Acessos Padrão

| Serviço         | URL                          |
| --------------- | ---------------------------- |
| Backend #1 API  | http://localhost:8002        |
| Backend #2 API  | http://localhost:8003        |
| Nginx Proxy     | http://localhost:8082        |
| Frontend Dev    | http://localhost:5176        |
| PostgreSQL GUI  | http://localhost:5051 (pgAdmin) |
| Prometheus      | http://localhost:9092        |
| Grafana         | http://localhost:3002        |

---

## Monitorização

- Prometheus (`9092`) coleta métricas de Redis, Nginx, backend  
- Grafana (`3002`) para dashboards interativos  

---

## Testes

### Backend

```bash
cd backend
pytest
```

### Load (k6)

```bash
cd backend/tests/load
./run_loadtest.sh
```

### Frontend

```bash
cd frontend
npm run test:coverage
```

---

## CI/CD

Workflows em `.github/workflows/`:

- **ci.yaml** – lint, testes unitários e build  
- **gen_openapi.yaml** – gera spec OpenAPI  
- **load_tests.yaml** – testes de carga (on-demand)  

---

## Contribuir

1. Fork & Clone  
2. `git checkout -b feat/minha-feature`  
3. Commit & Push  
4. Pull Request  

Use [Conventional Commits](https://www.conventionalcommits.org).  

---

## Licença

© 2025 Domínio Público (Unlicense). Veja [LICENSE](LICENSE).
