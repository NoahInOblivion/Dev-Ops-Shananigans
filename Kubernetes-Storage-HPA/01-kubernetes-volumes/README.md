# Kubernetes Volumes & Storage

## Overview
In Kubernetes, on-disk files in a container are ephemeral. When a container crashes or restarts, files are lost. Kubernetes volumes solve this problem by providing persistent data beyond individual container lifecycles.

---

## 1. emptyDir
- **Scope:** Bound to the Pod lifecycle.
- **Behavior:** Created when a Pod is assigned to a node; exists as long as that Pod is running on that node. If the Pod is deleted, the data in `emptyDir` is deleted permanently.
- **Primary Use Cases:**
  - Scratch space (sorting algorithms, disk-based caches).
  - Checkpointing long computations for crash recovery.
  - Shared storage between multiple containers in the same Pod (e.g. sidecar log collector).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-demo
spec:
  containers:
    - name: writer
      image: busybox
      command: ["/bin/sh", "-c", "echo 'Hello from emptyDir' > /cache/data.txt && sleep 3600"]
      volumeMounts:
        - name: cache-volume
          mountPath: /cache
  volumes:
    - name: cache-volume
      emptyDir: {}
```

---

## 2. hostPath
- **Scope:** Mounts a file or directory from the host node's filesystem into the Pod.
- **Behavior:** Data persists on the node even if the Pod is deleted. However, if the Pod is rescheduled onto another worker node, it will not find the data.
- **Primary Use Cases:**
  - Running cluster components (e.g. DaemonSets reading node `/var/log/pods`).
  - Accessing Docker socket or container runtime socket on the node.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-demo
spec:
  containers:
    - name: log-reader
      image: busybox
      command: ["/bin/sh", "-c", "ls -l /host-logs && sleep 3600"]
      volumeMounts:
        - name: host-log-volume
          mountPath: /host-logs
  volumes:
    - name: host-log-volume
      hostPath:
        path: /var/log
        type: Directory
```

---

## 3. PersistentVolume (PV) vs PersistentVolumeClaim (PVC)
- **PersistentVolume (PV):** A piece of storage in the cluster provisioned by an administrator or dynamically provisioned using a StorageClass. It has an independent lifecycle from any Pod that consumes it.
- **PersistentVolumeClaim (PVC):** A request for storage by a user. It specifies size, access modes (`ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`), and optional StorageClass.
- **Relationship:** Pods consume storage by referencing a PVC; Kubernetes binds the PVC to a matching PV.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

---

## 4. StorageClass & Dynamic Provisioning
- **StorageClass:** Defines the provisioner (e.g. AWS EBS, GCP PD, Azure Disk, local hostpath provisioner) and parameters for creating storage on-demand.
- **Dynamic Provisioning:** Instead of cluster administrators manually creating dozens of PVs beforehand, Kubernetes automatically provisions the underlying storage volume when a user creates a PVC referencing the StorageClass.

In Minikube, the built-in storage class is `standard` (or `k8s.io/minikube-hostpath`).
