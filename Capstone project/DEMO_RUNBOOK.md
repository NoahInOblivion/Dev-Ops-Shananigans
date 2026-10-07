# TaskBoard live demo

## Local application

```bash
cp .env.example .env
docker compose up --build -d
curl http://localhost:8000/health
open http://localhost:8080
docker compose down -v
```

## CI/CD story

Push a commit. GitHub Actions runs tests and the frontend build, builds both
images, scans HIGH/CRITICAL findings with Trivy, publishes SHA-tagged images,
then loads them into Kind and checks readiness plus `/health`.

## Failure scenarios

- `broken-image.yaml`: `kubectl describe pod` shows `ImagePullBackOff`; inspect
  the image name and registry credentials.
- `broken-service.yaml`: `kubectl get endpoints broken-service` is empty;
  compare the Service selector with Pod labels.
- A crashing container: `kubectl logs deployment/<name> --previous` and
  `kubectl describe pod` identify startup/configuration errors.

## Monitoring and cleanup

Install the stack using `monitoring/README.md`, import the dashboard, run
`./scripts/load-test.sh`, and watch request rate/latency. Remove demo resources
with `docker compose down -v` or `kubectl delete namespace taskboard`.
