#!/usr/bin/env bash
set -e

echo "=== 1. Initial Desired State applied from Git manifests ==="
kubectl apply -f Monitoring-and-GitOps/gitops-app/deployment.yaml
kubectl rollout status deployment/gitops-workload --timeout=60s
echo "Current replicas according to Git:"
kubectl get deployment gitops-workload -o jsonpath='Desired replicas: {.spec.replicas}, Available: {.status.availableReplicas}{"\n"}'

echo ""
echo "=== 2. Simulating Manual Configuration Drift (Out-of-Sync) ==="
echo "Ad-hoc manual scaling to 5 replicas..."
kubectl scale deployment gitops-workload --replicas=5
kubectl get deployment gitops-workload -o jsonpath='Drifted replicas: {.spec.replicas}{"\n"}'

echo ""
echo "=== 3. GitOps Continuous Reconciliation (Self-Healing back to Desired State) ==="
echo "Reconciling live cluster state against Git declarative repository..."
kubectl apply -f Monitoring-and-GitOps/gitops-app/deployment.yaml --prune -l managed-by=gitops 2>/dev/null || kubectl apply -f Monitoring-and-GitOps/gitops-app/deployment.yaml
kubectl rollout status deployment/gitops-workload --timeout=60s
echo "Cluster reconciled back to Git source-of-truth:"
kubectl get deployment gitops-workload -o jsonpath='Reconciled replicas: {.spec.replicas}, Available: {.status.availableReplicas}{"\n"}'
kubectl get pods -l app=gitops-workload
