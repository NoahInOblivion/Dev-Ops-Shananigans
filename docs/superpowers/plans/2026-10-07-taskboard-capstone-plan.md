# TaskBoard DevSecOps Capstone Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a locally demonstrable TaskBoard platform with tested FastAPI and React applications, secured containers, CI/CD, Kubernetes/Helm, Terraform, observability, and a secrets guide.

**Architecture:** A FastAPI service owns task persistence and metrics. A Vite-built React app is served by unprivileged Nginx and calls the backend through `/api`. Compose is the local path; raw Kubernetes manifests support Kind smoke tests; Helm and Terraform describe deployable environments.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy, SQLite/PostgreSQL, Pytest, React 18, Vite, Docker Compose, GitHub Actions, Trivy, Kind, Kubernetes, Helm, Terraform, Prometheus, Grafana.

**Spec:** `docs/superpowers/specs/2026-10-07-taskboard-capstone-design.md`

## Global Constraints

- Project code lives under `Capstone project/`.
- No real credentials, API keys, passwords, or private keys are committed.
- Local development defaults to SQLite; deployment configuration supports PostgreSQL.
- Runtime application containers run as non-root users.
- CI scans images for HIGH and CRITICAL vulnerabilities with unfixed findings ignored.
- Terraform validation must not require AWS credentials; AWS provisioning is opt-in.
- Every non-trivial behavior gets at least one focused automated check.

## Review Focus

- Empty and populated task lists return stable JSON shapes; pin in backend API tests.
- Invalid status and missing task IDs return validation/404 responses; pin in backend API tests.
- Database configuration works for SQLite tests and PostgreSQL deployment values; pin in backend setup tests and Compose config.
- Unprivileged Nginx can serve the frontend on its configured port; pin in Docker inspection and smoke checks.
- CI and Terraform do not expose secrets or require credentials for static validation; pin in workflow/config checks and the secrets guide.

---

### Task 1: Backend application and test database

**Files:**
- Create: `Capstone project/backend/pyproject.toml`
- Create: `Capstone project/backend/app/main.py`
- Create: `Capstone project/backend/app/config.py`
- Create: `Capstone project/backend/app/database.py`
- Create: `Capstone project/backend/app/models.py`
- Create: `Capstone project/backend/app/schemas.py`
- Create: `Capstone project/backend/app/metrics.py`
- Create: `Capstone project/backend/tests/conftest.py`
- Create: `Capstone project/backend/tests/test_api.py`

**Interfaces:**
- Produces FastAPI routes `/health`, `/`, `/api/tasks`, `/api/tasks/stats`, `/api/tasks/{task_id}`, and `/metrics`.
- `Task.status` accepts `TODO`, `IN_PROGRESS`, or `DONE`; missing tasks return 404.
- Tests override the database dependency with an isolated SQLite database.

- [ ] **Step 1: Write failing API tests** for health/root, empty and populated task lists, task creation validation, stats, update persistence, delete behavior, and missing-task handling.
- [ ] **Step 2: Run `cd 'Capstone project/backend' && pytest -q`** and confirm the tests fail because the app is absent.
- [ ] **Step 3: Implement the minimal SQLAlchemy model, Pydantic schemas, database session, CRUD routes, and Prometheus middleware/endpoint.** Keep SQLite as the default and read `DATABASE_URL` from environment.
- [ ] **Step 4: Run `pytest -q`** and confirm all tests pass.
- [ ] **Step 5: Run `python -m compileall app`** as a syntax check.

### Task 2: Frontend TaskBoard

**Files:**
- Create: `Capstone project/frontend/package.json`
- Create: `Capstone project/frontend/index.html`
- Create: `Capstone project/frontend/src/main.jsx`
- Create: `Capstone project/frontend/src/App.jsx`
- Create: `Capstone project/frontend/src/styles.css`
- Create: `Capstone project/frontend/vite.config.js`

**Interfaces:**
- Consumes the backend API through `/api` using a Vite development proxy and same-origin production routing.
- Produces a board with task creation, three status columns, status changes, deletion, and visible loading/error states.

- [ ] **Step 1: Add the smallest React app and scripts** for `npm run dev` and `npm run build`.
- [ ] **Step 2: Implement API calls and board state** in `App.jsx`, including form validation and accessible button labels.
- [ ] **Step 3: Add plain CSS** for a responsive three-column board; avoid a UI dependency.
- [ ] **Step 4: Run `cd 'Capstone project/frontend' && npm install && npm run build`** and confirm the production bundle succeeds.

### Task 3: Local containers and Compose

**Files:**
- Create: `Capstone project/backend/Dockerfile`
- Create: `Capstone project/backend/.dockerignore`
- Create: `Capstone project/frontend/Dockerfile`
- Create: `Capstone project/frontend/nginx.conf`
- Create: `Capstone project/docker-compose.yml`
- Create: `Capstone project/.env.example`

**Interfaces:**
- Backend listens on port 8000 as a non-root user.
- Frontend listens on unprivileged Nginx port 8080 and proxies `/api` to `backend:8000`.
- Compose supplies PostgreSQL and the backend `DATABASE_URL` without committing credentials.

- [ ] **Step 1: Create the backend image** with a fixed non-root user and a health endpoint.
- [ ] **Step 2: Create the unprivileged frontend image** using `nginxinc/nginx-unprivileged` and port 8080.
- [ ] **Step 3: Add Compose, PostgreSQL health checks, and `.env.example`.**
- [ ] **Step 4: Run `docker compose config`** and inspect the rendered services and ports.
- [ ] **Step 5: Run `docker compose up --build -d`, curl `/health` and `/`, then run `docker compose down -v`.**

### Task 4: CI/CD and DevSecOps gates

**Files:**
- Create: `Capstone project/.github/workflows/ci-cd.yml`
- Create: `Capstone project/k8s/namespace.yaml`
- Create: `Capstone project/k8s/backend.yaml`
- Create: `Capstone project/k8s/frontend.yaml`
- Create: `Capstone project/k8s/postgres.yaml`
- Create: `Capstone project/k8s/ingress.yaml`

**Interfaces:**
- Workflow runs backend tests and frontend build before image publication.
- Images use `${{ github.sha }}` tags and are scanned before push.
- Kind deploy waits for readiness and checks backend health plus frontend HTTP response.

- [ ] **Step 1: Add Kubernetes manifests** with probes, resource requests/limits, non-root security contexts, ConfigMap/Secret references, and backend HPA.
- [ ] **Step 2: Add the GitHub Actions quality/build/Trivy jobs** using the repository’s built-in token for GHCR.
- [ ] **Step 3: Add the Kind deploy/smoke job** with explicit cleanup.
- [ ] **Step 4: Run `kubectl apply --dry-run=client -f k8s/` where available** and inspect the workflow YAML for unquoted secret leakage.

### Task 5: Helm chart

**Files:**
- Create: `Capstone project/helm/taskboard/Chart.yaml`
- Create: `Capstone project/helm/taskboard/values.yaml`
- Create: `Capstone project/helm/taskboard/templates/_helpers.tpl`
- Create: `Capstone project/helm/taskboard/templates/backend.yaml`
- Create: `Capstone project/helm/taskboard/templates/frontend.yaml`
- Create: `Capstone project/helm/taskboard/templates/postgres.yaml`
- Create: `Capstone project/helm/taskboard/templates/ingress.yaml`
- Create: `Capstone project/helm/taskboard/templates/hpa.yaml`
- Create: `Capstone project/helm/taskboard/templates/config.yaml`

**Interfaces:**
- Values control image repositories/tags, replica counts, ingress host, resource settings, and database secret name.
- Templates render the same runtime contracts as the raw Kind manifests.

- [ ] **Step 1: Create the chart and values** with safe development defaults.
- [ ] **Step 2: Add templates** for Deployments, Services, ConfigMap/Secret references, Ingress, and HPA.
- [ ] **Step 3: Run `helm lint helm/taskboard`** and `helm template taskboard helm/taskboard`.

### Task 6: Terraform AWS definition

**Files:**
- Create: `Capstone project/terraform/versions.tf`
- Create: `Capstone project/terraform/variables.tf`
- Create: `Capstone project/terraform/main.tf`
- Create: `Capstone project/terraform/outputs.tf`
- Create: `Capstone project/terraform/terraform.tfvars.example`
- Create: `Capstone project/terraform/README.md`

**Interfaces:**
- Variables cover region, environment, cluster name, VPC CIDR, and subnet ranges.
- The configuration describes a VPC and EKS cluster with managed nodes, without embedding credentials.

- [ ] **Step 1: Write provider/version constraints and variables** with safe defaults.
- [ ] **Step 2: Add VPC, EKS, IAM, and outputs** using maintained Terraform AWS modules or direct resources only where required.
- [ ] **Step 3: Add `terraform.tfvars.example`** containing placeholders and comments, never secrets.
- [ ] **Step 4: Document `terraform init`, `fmt`, `validate`, `plan`, `apply`, and `destroy`, including cost warnings.**
- [ ] **Step 5: Run `terraform fmt -check` and `terraform validate`** when Terraform/provider plugins are available.

### Task 7: Observability assets

**Files:**
- Create: `Capstone project/monitoring/prometheus-values.yaml`
- Create: `Capstone project/monitoring/grafana-dashboard.json`
- Create: `Capstone project/monitoring/README.md`

**Interfaces:**
- Prometheus scrapes the backend `/metrics` endpoint.
- Dashboard panels cover request rate, errors, p50/p95/p99 latency, CPU, and memory.

- [ ] **Step 1: Add scrape values** for kube-prometheus-stack and the TaskBoard ServiceMonitor.
- [ ] **Step 2: Add a dashboard JSON export** using PromQL expressions matching the backend metric names.
- [ ] **Step 3: Document install, import, and verification commands** without requiring a hosted monitoring service.
- [ ] **Step 4: Validate the dashboard is valid JSON** with `python -m json.tool monitoring/grafana-dashboard.json`.

### Task 8: Troubleshooting, secrets guide, and project README

**Files:**
- Create: `Capstone project/troubleshooting/broken-image.yaml`
- Create: `Capstone project/troubleshooting/broken-service.yaml`
- Create: `Capstone project/scripts/load-test.sh`
- Create: `Capstone project/DEMO_RUNBOOK.md`
- Create: `Capstone project/SECRETS_GUIDE.md`
- Create: `Capstone project/README.md`

**Interfaces:**
- The guide clearly separates no-secret local runs, optional GHCR credentials, and AWS credentials required only for real Terraform operations.
- The runbook covers startup, CI, Kind, monitoring, cleanup, ImagePullBackOff, CrashLoopBackOff, and selector mismatch diagnosis.

- [ ] **Step 1: Add deliberately broken manifests** with comments describing the expected failure.
- [ ] **Step 2: Add a bounded Bash load-test script** that uses curl and accepts URL/count arguments.
- [ ] **Step 3: Write `SECRETS_GUIDE.md`** covering `.env`, GitHub Actions secrets/GITHUB_TOKEN, AWS CLI profiles/environment variables, GitHub OIDC, least privilege, and `terraform destroy`.
- [ ] **Step 4: Write README and demo runbook** with exact commands and prerequisites.
- [ ] **Step 5: Run `shellcheck` when available and execute the load test against a running local backend.**

### Task 9: Whole-project verification

**Files:**
- Modify: `README.md` to link the new capstone directory
- Create: `Capstone project/Makefile`

- [ ] **Step 1: Add a small Makefile** exposing `test`, `frontend-build`, `compose-config`, `helm-lint`, and `validate` targets; do not hide required credentials.
- [ ] **Step 2: Link `Capstone project/` from the repository README.**
- [ ] **Step 3: Run the available checks:** backend pytest, frontend build, Compose config, JSON validation, Helm lint, Terraform fmt/validate, and Kubernetes client-side validation.
- [ ] **Step 4: Run `git diff --check` and inspect `git status --short`.**
- [ ] **Step 5: Confirm the secrets scan finds no credentials** using targeted searches for common token/key patterns.

