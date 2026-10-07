# TaskBoard DevSecOps Capstone Design

**Date:** 2026-10-07  
**Project directory:** `Capstone project/`

## Goal

Build a small, locally demonstrable TaskBoard platform that shows the full
DevSecOps path from tested application code to secured containers and
Kubernetes-ready deployment artifacts, while closing every gap identified in
`PROJECT_REPORT.md`.

## Scope

The project will contain:

- A FastAPI backend with task CRUD operations, status statistics, health, and
  Prometheus metrics.
- A React/Vite frontend with a simple Kanban board, task creation, status
  changes, and deletion.
- SQLite for the default local/test database and PostgreSQL-compatible
  configuration for Compose/Kubernetes.
- Docker Compose for local full-stack execution.
- Non-root backend and frontend containers.
- Pytest coverage of at least six behaviors across at least three endpoints.
- GitHub Actions for tests, frontend build, image build, Trivy scanning, and a
  Kind smoke deployment.
- Kubernetes manifests and a Helm chart for the application.
- Terraform AWS configuration with safe example variables and no credentials.
- Prometheus scrape configuration, a Grafana dashboard JSON export, and
  verification instructions.
- Troubleshooting manifests and a live demo runbook.

Explicitly out of scope for the first implementation:

- Real AWS provisioning or committed cloud credentials.
- Authentication, multi-tenancy, billing, or user accounts.
- A custom design system or frontend component library.
- Production-grade PostgreSQL backup, migration orchestration, or HA.

## Architecture

The backend is a single FastAPI service using SQLAlchemy models and a small
database abstraction. The default `DATABASE_URL` points to SQLite so tests and
local runs need no external service; Compose and Kubernetes provide PostgreSQL
configuration. The frontend is a static Vite build served by an unprivileged
Nginx image and calls the backend through `/api`.

The delivery path is:

```text
commit -> backend tests + frontend build -> Docker build -> Trivy scan
       -> image publish (SHA tag) -> Kind deploy -> health/smoke checks
```

The Helm chart is the deployable Kubernetes package. Raw manifests remain for
the CI Kind smoke test. Terraform provisions the AWS network and EKS shape but
is not executed as part of local verification.

## Application behavior

Tasks have an integer ID, title, optional description, status, and timestamps.
Valid statuses are `TODO`, `IN_PROGRESS`, and `DONE`. The API exposes:

- `GET /health`
- `GET /`
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/stats`
- `PUT /api/tasks/{task_id}`
- `DELETE /api/tasks/{task_id}`
- `GET /metrics`

Invalid input returns a validation error. Missing tasks return HTTP 404.
Stats include `total` and counts for each valid status.

## Security and reliability requirements

- Application containers run as non-root users.
- Backend input validation is enforced at the API boundary.
- No secrets or real credentials are committed.
- Images are scanned for HIGH and CRITICAL vulnerabilities in CI, ignoring
  only unfixed vulnerabilities as specified by the report.
- Kubernetes deployments include readiness and liveness probes, resource
  requests/limits, and a backend HPA.
- Kubernetes configuration uses Secrets/ConfigMaps for runtime values rather
  than hard-coded application credentials.
- The frontend remains accessible without JavaScript-only navigation or
  inaccessible controls.

## Observability

The backend records request count and latency metrics using the existing
Prometheus ecosystem available to the Python service. The dashboard export
will include request rate, 4xx/5xx rate, latency percentiles, and process
resource panels. Documentation will show how to install the monitoring stack,
import the dashboard, and verify `/metrics`.

## Verification

The project is complete when these checks are documented and pass where the
required tools are installed:

1. Backend tests pass with `pytest`.
2. Frontend production build passes with `npm run build`.
3. `docker compose config` succeeds and both images declare non-root runtime
   users.
4. Terraform formatting and validation pass without requiring AWS credentials.
5. Helm lint succeeds.
6. Kind smoke deployment reaches ready state and verifies `/health` and the
   frontend route.
7. The runbook explains local startup, CI behavior, monitoring, cleanup, and
   three troubleshooting scenarios.

## Secrets and credentials

The application needs no API key for local development. The local Compose
database uses development-only credentials from an ignored `.env` file or
documented defaults; no secret values are committed.

The CI workflow requires registry credentials only when publishing images:
`REGISTRY_USERNAME` and `REGISTRY_TOKEN`. GitHub's built-in `GITHUB_TOKEN` may
be used for GHCR, so these are optional when GHCR is the selected registry.

Terraform validation and formatting require no AWS credentials. A real
`terraform plan` or `apply` requires AWS credentials configured in the shell or
through GitHub OIDC. The guide will cover `aws configure`, environment
variables, the safer OIDC path, least-privilege permissions, and the
cost-bearing `apply`/`destroy` workflow. No access keys, tokens, passwords, or
private keys will be placed in the repository.

## Deliberate simplifications

- SQLite is the default development database because it removes setup cost;
  PostgreSQL is retained as the deployment path.
- Terraform is a reproducible infrastructure definition, not an invitation to
  spend money during verification.
- The frontend is intentionally small; the capstone demonstrates delivery and
  operations rather than product breadth.
