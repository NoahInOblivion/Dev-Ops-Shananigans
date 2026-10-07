# TaskBoard DevSecOps Capstone

TaskBoard is a small FastAPI + React application used to demonstrate the
delivery path in `PROJECT_REPORT.md`: tests, non-root images, Trivy, GitHub
Actions, Kind, Kubernetes, Helm, Terraform, and Prometheus/Grafana.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Open <http://localhost:8080>. Backend API docs are at
<http://localhost:8000/docs>.

## Checks

```bash
cd backend && python -m pytest -q
cd ../frontend && npm ci && npm run build
```

See [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) for the full demo and
[SECRETS_GUIDE.md](SECRETS_GUIDE.md) before using AWS or another registry.
