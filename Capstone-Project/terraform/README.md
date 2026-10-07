# Terraform AWS infrastructure

This directory describes an AWS VPC and EKS cluster. It does not create
anything until `terraform apply` is run.

```bash
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check
terraform validate
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
terraform destroy -var-file=terraform.tfvars
```

`fmt`, `validate`, and the example file require no AWS credentials. `plan` and
`apply` do. Use an AWS CLI profile or environment credentials locally; use
GitHub OIDC rather than long-lived access keys in CI. Start with the minimum
permissions needed for the VPC/EKS modules, set a budget alert, and always
destroy the development cluster when finished. Never commit `terraform.tfvars`.
