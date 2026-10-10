#!/usr/bin/env bash
set -e

echo "=== 1. Linting & Packaging TaskBoard Helm Chart ==="
helm lint Capstone-Project/helm/taskboard
helm package Capstone-Project/helm/taskboard -d /tmp/

echo ""
echo "=== 2. Deploying TaskBoard Complete Kubernetes Stack ==="
kubectl create namespace taskboard --dry-run=client -o yaml | kubectl apply -f -

cat << 'MANIFESTS' | kubectl apply -n taskboard -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: taskboard-config
data:
  DATABASE_URL: "postgresql+psycopg://taskboard:change-me@postgres:5432/taskboard"
  LOG_LEVEL: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: taskboard-db
type: Opaque
stringData:
  POSTGRES_PASSWORD: "change-me"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskboard-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: taskboard-backend
  template:
    metadata:
      labels:
        app: taskboard-backend
    spec:
      containers:
      - name: backend
        image: nginx:1.25-alpine
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 50m
            memory: 32Mi
          limits:
            cpu: 200m
            memory: 64Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 2
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: taskboard-backend
spec:
  selector:
    app: taskboard-backend
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskboard-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: taskboard-frontend
  template:
    metadata:
      labels:
        app: taskboard-frontend
    spec:
      containers:
      - name: frontend
        image: nginx:1.24-alpine
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 50m
            memory: 32Mi
          limits:
            cpu: 200m
            memory: 64Mi
---
apiVersion: v1
kind: Service
metadata:
  name: taskboard-frontend
spec:
  selector:
    app: taskboard-frontend
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: taskboard-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: taskboard-backend
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
MANIFESTS

echo ""
echo "=== 3. Verifying All Kubernetes Resources in 'taskboard' Namespace ==="
kubectl -n taskboard rollout status deployment/taskboard-backend --timeout=60s
kubectl -n taskboard rollout status deployment/taskboard-frontend --timeout=60s

echo ""
echo "--- Deployments & Pods ---"
kubectl -n taskboard get deployments,pods

echo ""
echo "--- Services & ClusterIP Networking ---"
kubectl -n taskboard get services

echo ""
echo "--- ConfigMaps & Secrets ---"
kubectl -n taskboard get configmaps,secrets

echo ""
echo "--- HorizontalPodAutoscaler (HPA) ---"
kubectl -n taskboard get hpa
