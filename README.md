# Tarefas API - CI com GitHub Actions

API REST de tarefas (Node.js + Express + PostgreSQL) com pipeline de Integração Contínua.

## Endpoints

| Método | Rota       | Descrição        |
| ------ | ---------- | ---------------- |
| GET    | /health    | Status da API    |
| GET    | /tasks     | Lista tarefas    |
| GET    | /tasks/:id | Busca uma tarefa |
| POST   | /tasks     | Cria tarefa      |
| PUT    | /tasks/:id | Atualiza tarefa  |
| DELETE | /tasks/:id | Remove tarefa    |

## Rodar localmente

```bash
docker compose up --build
curl -X POST localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"Estudar CI"}'
curl localhost:3000/tasks
```

## Scripts

`npm run lint` | `npm run format:check` | `npm run build` | `npm run test:unit` | `npm run test:integration`

## Pipeline (.github/workflows/ci.yml)

Gatilho: Pull Request para `main`.
`lint` + `format` + `security` (em paralelo) -> `build` -> `unit-test` -> `integration-test` -> `docker`
