#!/usr/bin/env bash
set -e

echo "=== Deploying Monitored Application ==="
kubectl apply -f Monitoring-and-GitOps/monitoring-demo/monitored-app.yaml

echo "=== Waiting for rollout ==="
kubectl rollout status deployment/monitored-app --timeout=60s

echo "=== Waiting for metrics-server scrape window (30s) ==="
sleep 30

echo ""
echo "=== 1. Node & Pod Metrics (CPU & Memory Utilization) ==="
kubectl top nodes
kubectl top pod -l app=monitored-app || (sleep 10 && kubectl top pod -l app=monitored-app)

echo ""
echo "=== 2. Application Health & Readiness/Liveness Probes ==="
kubectl get pods -l app=monitored-app -o wide

echo ""
echo "=== 3. Container Application Logs ==="
kubectl logs -l app=monitored-app --tail=6
