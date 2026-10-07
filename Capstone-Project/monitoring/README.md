# Monitoring

Install the community stack into a cluster:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  -f monitoring/prometheus-values.yaml
```

Expose Grafana with `kubectl port-forward svc/monitoring-grafana 3000:80` and
retrieve its generated admin password from the chart's Kubernetes Secret.
Import `grafana-dashboard.json`, then verify the backend's `/metrics` endpoint
and the `http_requests_total` and `http_request_duration_seconds` series.
