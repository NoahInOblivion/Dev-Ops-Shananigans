# Secrets and API keys

## Local development

No API key is needed. Copy `.env.example` to `.env`, change the local database
password if using Compose, and keep `.env` untracked. SQLite backend tests need
no environment variables.

## GitHub Actions

The workflow uses the short-lived built-in `GITHUB_TOKEN` to publish to GHCR,
so no registry secret is required for this repository. If another registry is
chosen, add `REGISTRY_USERNAME` and `REGISTRY_TOKEN` under repository Settings →
Secrets and variables → Actions, then reference them only in the login step.

Never print a secret or pass it as a Docker build argument.

## AWS and Terraform

Static Terraform formatting and validation need no credentials. A real plan or
apply needs AWS access. For local work, prefer a named profile:

```bash
aws configure --profile taskboard-dev
export AWS_PROFILE=taskboard-dev
cd terraform
terraform plan -var-file=terraform.tfvars
```

For CI, prefer GitHub OIDC with an AWS IAM role restricted to the repository
and environment. Do not create long-lived access keys as GitHub secrets unless
OIDC is unavailable. Review the IAM policy, set an AWS budget alert, and run:

```bash
terraform destroy -var-file=terraform.tfvars
```

after the demo. `terraform.tfvars`, state files, and `.env` are ignored and
must never be committed.
