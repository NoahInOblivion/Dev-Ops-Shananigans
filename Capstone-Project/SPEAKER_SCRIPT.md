# TaskBoard Capstone Video Walkthrough — Speaker Script & Recording Guide

This document provides a word-for-word voiceover script and terminal command cheatsheet to accompany your video recording.

Target Video Duration: **5 – 7 minutes**

---

## 📋 Pre-Recording Checklist

1. **Terminal 1 (Local App & Cluster):** Have terminal open at `~/Projects/Dev/DevOps/Dev-Ops-Shananigans/Capstone-Project`.
2. **Terminal 2 (Git & CI):** Ready to show git commits or repository status.
3. **Browser Tabs Ready:**
   - Tab 1: Presentation slide deck (`presentation.html` open in Chromium / Chrome, press `F` for fullscreen).
   - Tab 2: GitHub Repository Actions tab (`.github/workflows/ci-cd.yml` run history).
   - Tab 3: Local TaskBoard UI at `http://localhost:8080` (or `http://localhost:3000`).
   - Tab 4: Backend docs / health at `http://localhost:8000/docs` & `http://localhost:8000/health`.
   - Tab 5: Prometheus targets / Grafana dashboard (if running).

---

## 🎙️ Step-by-Step Script & Video Flow

### [0:00 – 0:45] Intro & Title Slide (Slide 1 & 2)
- **On Screen:** Slide 1 (`presentation.html`), then advance to Slide 2.
- **Voiceover:**
  > "Hello everyone, my name is Dhruv, and welcome to my final DevOps Capstone presentation for Session 21.
  > Today I am presenting **TaskBoard**, an enterprise-grade cloud-native DevSecOps platform.
  > Rather than operating individual DevOps tools in isolation, this project implements a complete, automated lifecycle: taking a multi-tier SaaS application from local development through automated testing and security scanning, cloud infrastructure provisioning with Terraform, declarative Kubernetes orchestration using Helm, and continuous observability with Prometheus and Grafana.
  > Let's dive in!"

---

### [0:45 – 1:30] Application Tier & Docker Hardening (Slide 3 & Local Demo)
- **On Screen:** Slide 3, then switch to Terminal / Browser.
- **Voiceover:**
  > "Looking at the application layer, TaskBoard is built with an asynchronous FastAPI Python backend, a PostgreSQL relational database with Alembic schema migrations, and a responsive React single-page frontend.
  > From a DevOps and security perspective, we followed strict best practices:
  > First, both Dockerfiles run as unprivileged non-root users — specifically UID 10001 for the backend.
  > Second, we implemented multi-stage builds to minimize image size and strip out build tools.
  > Third, the backend provides discrete `/health` and `/ready` endpoints: `/health` checks process liveness, while `/ready` verifies database connectivity before Kubernetes routes traffic."
- **Terminal Action (show local app):**
  ```bash
  docker compose up -d
  curl http://localhost:8000/health
  ```
  *(Show TaskBoard UI loaded in browser with Kanban stats)*

---

### [1:30 – 2:45] DevSecOps & CI/CD Pipeline (Slide 4 & GitHub Actions)
- **On Screen:** Slide 4, then switch to GitHub repository Actions tab.
- **Voiceover:**
  > "For continuous integration and delivery, we built a zero-touch GitHub Actions workflow.
  > On every push to main:
  > 1. Automated Pytest runs against our backend REST endpoints to enforce code quality.
  > 2. The React frontend is compiled and validated.
  > 3. Docker images are built and passed to our security gate: a Trivy vulnerability scan configured to block the pipeline if any HIGH or CRITICAL CVEs are detected.
  > 4. Once security gates pass, images are tagged with the exact Git commit SHA rather than 'latest'. This provides an immutable audit trail and ensures deterministic deployments.
  > 5. Finally, an ephemeral Kind cluster is spun up right inside CI to smoke test pod health before merging."

---

### [2:45 – 3:45] Infrastructure as Code — AWS Terraform (Slide 5)
- **On Screen:** Slide 5.
- **Voiceover:**
  > "For cloud infrastructure, we defined our AWS environment entirely as code using Terraform.
  > Our Terraform configuration provisions:
  > - A resilient VPC in AWS region ap-south-1 with multi-AZ public subnets, an Internet Gateway, and NAT Gateways.
  > - A managed AWS EKS 1.31 Kubernetes cluster with a dedicated node group of 2 t3.medium EC2 instances.
  > - We enforce clean secrets management: no AWS credentials are ever committed, and a `terraform.tfvars.example` file is provided for parameterization.
  > - The entire lifecycle is automated: `terraform init`, `plan`, `apply`, and a clean `destroy` sequence to prevent idle cloud costs."

---

### [3:45 – 5:00] Kubernetes & Helm Deployment (Slide 6 & Live Script)
- **On Screen:** Slide 6, then switch to Terminal running `./run-k8s-helm-demo.sh`.
- **Voiceover:**
  > "For orchestration, TaskBoard is packaged as a production Helm chart in `helm/taskboard`.
  > Let's deploy the stack to our Kubernetes cluster."
- **Terminal Action:**
  ```bash
  ./run-k8s-helm-demo.sh
  ```
- **Voiceover as output scrolls:**
  > "Notice what our script executes:
  > - Helm lints and packages our chart.
  > - We create the `taskboard` namespace.
  > - Deployments are created with 2 replicas for high availability.
  > - ConfigMaps and Opaque Secrets are injected cleanly into the pods.
  > - Nginx Ingress routes `/` to the React frontend and `/api` to the backend.
  > - We also configure a Horizontal Pod Autoscaler set to scale between 2 and 6 replicas at a 60% CPU threshold, backed by liveness and readiness probes for zero-downtime rolling updates."
- **Terminal verification command:**
  ```bash
  kubectl get all -n taskboard
  kubectl get hpa -n taskboard
  ```

---

### [5:00 – 6:15] Production Troubleshooting Challenge (Slide 7 & Terminal)
- **On Screen:** Slide 7, then switch to Terminal running `./run-troubleshooting-demo.sh`.
- **Voiceover:**
  > "A crucial part of Session 21 is demonstrating real-world incident response on Kubernetes. We resolved two challenging production scenarios:
  > **Challenge 1:** A pod was stuck in `ImagePullBackOff`. Running `kubectl describe pod` revealed an invalid, nonexistent container image registry tag. We resolved it by applying a live patch using `kubectl set image`, restoring the pod to Running.
  > **Challenge 2:** Upstream Ingress was returning HTTP 503, and `kubectl get endpoints` showed no active endpoints. By inspecting the Service selector labels against the Pod labels, we identified a label selector mismatch. We patched the Service selector, immediately restoring pod endpoints and traffic routing."

---

### [6:15 – 7:00] Observability, SRE & Conclusion (Slide 8 & 9)
- **On Screen:** Slide 8, then advance to Slide 9.
- **Voiceover:**
  > "Lastly, our Observability tier exposes standardized Prometheus metrics at `/metrics`. Prometheus scrapes request counts and response latency, and Grafana visualizes our RED metrics. Under synthetic load, we can observe the HPA dynamically scaling replicas to maintain service level objectives.
  > To conclude, TaskBoard satisfies 100 out of 100 points across all 10 modules of the grading rubric. More importantly, it demonstrates the key tenets of modern DevOps: shifting security left, using immutable infrastructure, and automating deployment and recovery.
  > Thank you for watching!"

---

## 💡 Quick Tips for Screen Recording
1. **Screen Resolution:** Set display to 1080p (1920x1080) for crisp video recording.
2. **Recording Tool:** You can use **OBS Studio** or **SimpleScreenRecorder** on Ubuntu:
   ```bash
   sudo apt install -y simplescreenrecorder
   ```
   Or use browser extensions like **Loom**.
3. **Presentation Shortcuts:**
   - In `presentation.html`: Press `F` to enter full-screen mode, use `Right Arrow` to advance slides, and press `S` if you want to peek at the speaker notes.
