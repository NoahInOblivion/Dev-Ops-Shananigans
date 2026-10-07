.PHONY: test frontend-build compose-config helm-lint validate

test:
	cd backend && python -m pytest -q

frontend-build:
	cd frontend && npm run build

compose-config:
	docker compose config >/dev/null

helm-lint:
	helm lint helm/taskboard

validate: test frontend-build compose-config helm-lint
