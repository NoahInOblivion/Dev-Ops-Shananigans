#!/usr/bin/env bash
set -e

echo "=== Preparing Namespace ==="
kubectl create namespace taskboard-debug --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "=== Step 1: Reproducing Challenge 1 (Broken Image / ImagePullBackOff) ==="
cat << 'MANIFEST' | kubectl apply -n taskboard-debug -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: broken-image
spec:
  replicas: 1
  selector:
    matchLabels:
      app: broken-image
  template:
    metadata:
      labels:
        app: broken-image
    spec:
      containers:
      - name: app
        image: example.invalid/taskboard:nonexistent-tag
        imagePullPolicy: Always
MANIFEST

echo "Diagnosing broken-image pod..."
sleep 3
kubectl -n taskboard-debug get pods -l app=broken-image
echo "Root Cause Identified: Invalid container image registry tag leads to ImagePullBackOff."

echo ""
echo "=== Step 2: Fixing Challenge 1 in real-time ==="
echo "Updating deployment image to valid local image (nginx:1.25-alpine)..."
kubectl -n taskboard-debug set image deployment/broken-image app=nginx:1.25-alpine
kubectl -n taskboard-debug rollout status deployment/broken-image --timeout=30s
kubectl -n taskboard-debug get pods -l app=broken-image

echo ""
echo "=== Step 3: Reproducing Challenge 2 (Broken Service Selector / Missing Endpoints) ==="
cat << 'MANIFEST' | kubectl apply -n taskboard-debug -f -
apiVersion: v1
kind: Service
metadata:
  name: broken-service
spec:
  selector:
    app: misconfigured-label
  ports:
  - port: 80
    targetPort: 80
MANIFEST

echo "Checking Service Endpoints..."
kubectl -n taskboard-debug get endpoints broken-service
echo "Root Cause Identified: Service selector 'app: misconfigured-label' matches zero pods (Endpoints: <none>)."

echo ""
echo "=== Step 4: Fixing Challenge 2 in real-time ==="
echo "Patching Service selector to match active workload 'app: broken-image'..."
kubectl -n taskboard-debug patch service broken-service -p '{"spec":{"selector":{"app":"broken-image"}}}'
sleep 2
kubectl -n taskboard-debug get endpoints broken-service
echo "Service successfully attached to pod endpoints!"
