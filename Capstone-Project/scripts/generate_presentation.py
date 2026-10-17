import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_COLOR = RGBColor(15, 23, 42)        # #0f172a (Deep Slate)
    CARD_BG = RGBColor(30, 41, 59)        # #1e293b (Slate 800)
    CARD_BORDER = RGBColor(51, 65, 85)    # #334155 (Slate 700)
    TEXT_PRIMARY = RGBColor(248, 250, 252)# #f8fafc (Slate 50)
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94a3b8 (Slate 400)
    ACCENT_CYAN = RGBColor(56, 189, 248)  # #38bdf8 (Sky 400)
    ACCENT_PURPLE = RGBColor(129, 140, 248)# #818cf8 (Indigo 400)
    ACCENT_GREEN = RGBColor(52, 211, 153) # #34d399 (Emerald 400)
    ACCENT_AMBER = RGBColor(251, 191, 36) # #fbbf24 (Amber 400)

    slides_data = [
        {
            "tag": "CAPSTONE PROJECT • SESSION 21",
            "title": "TaskBoard: Cloud-Native DevSecOps Platform",
            "subtitle": "End-to-End Automated CI/CD, Container Security, AWS Infrastructure as Code, Kubernetes Orchestration & Observability",
            "type": "title",
            "cards": [
                {"title": "FastAPI + React + Postgres", "desc": "3-Tier Microservice with Alembic migrations and non-root containers", "color": ACCENT_CYAN},
                {"title": "DevSecOps CI/CD", "desc": "GitHub Actions + Trivy vulnerability scanning + GHCR SHA-tagging", "color": ACCENT_PURPLE},
                {"title": "Kubernetes & Helm", "desc": "Multi-replica deployments, HPA, Ingress, and self-healing cluster runtime", "color": ACCENT_GREEN},
                {"title": "Terraform AWS & Metrics", "desc": "Modular VPC/EKS IaC + Prometheus metrics & Grafana telemetry", "color": ACCENT_AMBER}
            ],
            "notes": (
                "Welcome everyone. Today I am presenting my final DevOps Capstone project: TaskBoard. "
                "TaskBoard is a production-grade demonstration of modern cloud-native engineering and DevSecOps. "
                "Rather than treating tools in isolation, this project implements a complete pipeline that takes code "
                "from a developer's workstation, through rigorous security gates and automated testing, into an AWS EKS "
                "cluster managed declaratively by Helm and monitored continuously by Prometheus and Grafana."
            )
        },
        {
            "tag": "SYSTEM ARCHITECTURE",
            "title": "End-to-End Cloud-Native Architecture",
            "subtitle": "Declarative lifecycle from code commit to monitored Kubernetes runtime",
            "type": "split",
            "cards": [
                {"title": "1. Delivery Tier (CI/CD & Security)", "desc": "• Git Push to 'main' triggers GitHub Actions\n• Automated Pytest execution (SQLite/mock DB)\n• Multi-stage Docker builds (Backend & Frontend)\n• Trivy scans for HIGH/CRITICAL CVEs\n• Immutable GHCR image publishing tagged with Git commit SHA", "color": ACCENT_CYAN},
                {"title": "2. Infrastructure Tier (AWS & Terraform)", "desc": "• Automated VPC across multiple availability zones\n• Public/Private subnets, Internet & NAT Gateways\n• Managed AWS EKS 1.31 cluster with 2x t3.medium nodes\n• Safe state management & clean terraform destroy lifecycle", "color": ACCENT_PURPLE},
                {"title": "3. Orchestration Tier (Kubernetes & Helm)", "desc": "• Packaged via custom Helm chart (helm/taskboard)\n• Decoupled ConfigMaps and Opaque Secrets\n• Dual-replica deployments with Liveness & Readiness probes\n• Nginx Ingress routing (/ -> UI, /api -> Backend)\n• Horizontal Pod Autoscaler (2-6 replicas at 60% CPU)", "color": ACCENT_GREEN},
                {"title": "4. Observability & SRE Tier", "desc": "• FastAPI Prometheus instrumentator at /metrics\n• Prometheus server scraping ServiceMonitors\n• Grafana dashboards tracking request throughput, latency (p95), and HTTP error codes\n• Automated rolling updates with zero downtime", "color": ACCENT_AMBER}
            ],
            "notes": (
                "Here is our high-level architecture diagram. It is organized into four interconnected tiers: "
                "First, our Delivery Tier runs on GitHub Actions, handling test automation, containerization, and DevSecOps scans. "
                "Second, our Infrastructure Tier is provisioned with Terraform on AWS, delivering an EKS cluster inside a secure VPC. "
                "Third, our Orchestration Tier uses Helm to manage multi-replica microservices, ingress routing, and autoscaling. "
                "Finally, our Observability Tier pulls metrics into Prometheus and Grafana for real-time SRE monitoring."
            )
        },
        {
            "tag": "APPLICATION & CONTAINERIZATION",
            "title": "Application Tier & Docker Best Practices",
            "subtitle": "Microservices built for scalability, resilience, and least-privilege security",
            "type": "cards_3",
            "cards": [
                {
                    "title": "FastAPI Backend",
                    "desc": "• High-performance asynchronous Python 3.12 API\n• 6 REST endpoints: GET, POST, PUT, DELETE, and /stats\n• Dedicated /health and /ready endpoints for Kubernetes probes\n• SQLAlchemy 2.0 ORM with Alembic schema migrations\n• Instrumented with Prometheus client middleware",
                    "color": ACCENT_CYAN
                },
                {
                    "title": "React Frontend & DB",
                    "desc": "• Single Page App built with React 18 and Vite\n• Real-time Kanban metrics: Total, To-Do, In-Progress, Done\n• Dynamic modal task creation and status updating\n• Nginx reverse proxy handles API routing seamlessly\n• PostgreSQL 16 Alpine persistent storage",
                    "color": ACCENT_PURPLE
                },
                {
                    "title": "Hardened Docker Containers",
                    "desc": "• Backend: Non-root user 'appuser' (UID 10001)\n• Frontend: Multi-stage build (Node compile + unprivileged Nginx runtime)\n• Minimal Alpine image bases for reduced attack surface\n• Docker Compose stack for 1-command local validation: docker compose up --build",
                    "color": ACCENT_GREEN
                }
            ],
            "notes": (
                "Looking at the application layer, TaskBoard is composed of a FastAPI backend and a React single-page frontend. "
                "Crucially for DevOps, the backend implements discrete /health and /ready endpoints. The health endpoint checks process liveness, "
                "while the readiness endpoint verifies active database connectivity before Kubernetes routes user traffic. "
                "For security, both containers run strictly as non-privileged non-root users, ensuring root privilege escalation inside containers is blocked."
            )
        },
        {
            "tag": "AUTOMATION & DEVSECOPS",
            "title": "Automated CI/CD & DevSecOps Pipeline",
            "subtitle": "Shift-left security and zero-touch continuous deployment via GitHub Actions",
            "type": "split",
            "cards": [
                {
                    "title": "Quality & Test Automation Gate",
                    "desc": "• Trigger: Automated execution on git push to main\n• Pytest suite runs against mock/isolated database\n• Validates CRUD endpoints, status transitions, and data integrity\n• Enforces automated failure: Pipeline blocks immediately if any test fails",
                    "color": ACCENT_CYAN
                },
                {
                    "title": "Trivy Security Vulnerability Gate",
                    "desc": "• Automated container scanning before publishing\n• Flags and blocks on HIGH and CRITICAL CVE vulnerabilities\n• Eliminates outdated vulnerable base dependencies\n• Guarantees security compliance prior to runtime deployment",
                    "color": ACCENT_PURPLE
                },
                {
                    "title": "Immutable GHCR Artifact Publishing",
                    "desc": "• Builds both backend and frontend images in parallel\n• Tags artifacts with the exact Git commit SHA (never generic 'latest')\n• Enables 100% reproducible deployments and instant rollbacks\n• Pushes signed images to GitHub Container Registry (GHCR)",
                    "color": ACCENT_GREEN
                },
                {
                    "title": "Ephemeral Verification (Kind Cluster)",
                    "desc": "• Spins up an ephemeral Kubernetes cluster (Kind) inside CI\n• Pre-loads built SHA-tagged images into cluster nodes\n• Applies Kubernetes manifests and checks pod readiness\n• Performs in-cluster curl smoke tests against /health and API",
                    "color": ACCENT_AMBER
                }
            ],
            "notes": (
                "Our continuous integration pipeline in GitHub Actions enforces our DevSecOps philosophy. "
                "First, Pytest executes as the quality gate. Next, images are built and scanned by Trivy for HIGH and CRITICAL vulnerabilities. "
                "Images are tagged strictly with the Git commit SHA rather than 'latest', providing an immutable audit trail. "
                "Finally, the pipeline spins up an ephemeral Kind cluster in the runner to test actual deployment readiness before merging."
            )
        },
        {
            "tag": "INFRASTRUCTURE AS CODE",
            "title": "Terraform: Cloud Infrastructure Automation",
            "subtitle": "Modular AWS infrastructure provisioning with zero manual console intervention",
            "type": "cards_3",
            "cards": [
                {
                    "title": "Modular VPC Design",
                    "desc": "• Multi-AZ networking in ap-south-1\n• Dual public and private subnets\n• Internet Gateway for inbound traffic\n• NAT Gateway for secure egress\n• Strict Security Group rules for least-privilege access",
                    "color": ACCENT_CYAN
                },
                {
                    "title": "AWS Managed EKS 1.31",
                    "desc": "• Production-ready Kubernetes control plane\n• Managed Node Group: 2x t3.medium EC2 instances\n• IAM roles and OIDC provider integration\n• Auto-scaling worker nodes with EBS storage provisioner",
                    "color": ACCENT_PURPLE
                },
                {
                    "title": "Clean IaC Lifecycle",
                    "desc": "• Parameterized via terraform.tfvars.example\n• Zero hardcoded credentials or cloud secrets\n• Reproducible workflow: terraform init -> plan -> apply\n• Verified teardown via terraform destroy to prevent idle cloud costs",
                    "color": ACCENT_AMBER
                }
            ],
            "notes": (
                "For infrastructure provisioning, we used Terraform to declare our AWS environment as code. "
                "The setup creates a resilient multi-AZ VPC equipped with public subnets, NAT gateways, and an EKS 1.31 managed cluster. "
                "The configuration follows industry standards: zero credentials in code, clear input variables with terraform.tfvars.example, "
                "and an verified destroy lifecycle ensuring all cloud resources can be cleanly decommissioned."
            )
        },
        {
            "tag": "KUBERNETES & PACKAGING",
            "title": "Kubernetes Orchestration & Helm Packaging",
            "subtitle": "Declarative microservice management, auto-scaling, and traffic routing",
            "type": "split",
            "cards": [
                {
                    "title": "Helm Chart Architecture (helm/taskboard)",
                    "desc": "• Reusable templating with Chart.yaml and values.yaml\n• Configurable resource requests and limits (CPU/Memory)\n• Support for multiple environments (dev, staging, prod)\n• One-command installation: helm upgrade --install taskboard ./helm/taskboard",
                    "color": ACCENT_CYAN
                },
                {
                    "title": "Reliability & Health Probes",
                    "desc": "• Liveness Probe: Monitors container responsiveness; restarts deadlocked pods\n• Readiness Probe: Validates DB connectivity before sending traffic\n• Rolling updates: MaxUnavailable=0, MaxSurge=1 for zero-downtime releases",
                    "color": ACCENT_PURPLE
                },
                {
                    "title": "Traffic Routing via Ingress",
                    "desc": "• Ingress controller routes hostname taskboard.local\n• Path-based routing: '/' routes to React frontend\n• '/api' routes traffic directly to FastAPI backend service\n• No internal service ports exposed directly to public internet",
                    "color": ACCENT_GREEN
                },
                {
                    "title": "Autonomous Scaling (HPA)",
                    "desc": "• Horizontal Pod Autoscaler targets CPU utilization at 60%\n• Automatically scales backend from 2 to 6 replicas under load\n• Kubernetes Metrics-Server feeds real-time pod resource telemetry\n• Verified through automated load-testing scripts",
                    "color": ACCENT_AMBER
                }
            ],
            "notes": (
                "Turning to Kubernetes runtime operations, our entire application is packaged as a Helm chart. "
                "We configure dual replicas for high availability, paired with liveness and readiness probes to guarantee zero-downtime rolling updates. "
                "An Nginx Ingress controller routes user traffic through a single entrypoint, directing UI requests to the frontend and API traffic to the backend. "
                "Under peak traffic, our Horizontal Pod Autoscaler automatically scales our backend pods from 2 up to 6 instances."
            )
        },
        {
            "tag": "ROOT CAUSE ANALYSIS",
            "title": "Production Kubernetes Troubleshooting Challenge",
            "subtitle": "Simulated real-world production incident response and resolution workflows",
            "type": "split",
            "cards": [
                {
                    "title": "Incident 1: ImagePullBackOff / ErrImagePull",
                    "desc": "• Symptom: Pod stuck in ErrImagePull, failing to reach Running status.\n• Root Cause Analysis: Executed kubectl describe pod; revealed invalid container image tag 'example.invalid/taskboard:nonexistent-tag'.\n• Resolution: Applied immediate live patch via kubectl set image deployment/broken-image to verified image nginx:1.25-alpine.\n• Result: Pod successfully pulled image and reached Running (1/1).",
                    "color": ACCENT_AMBER
                },
                {
                    "title": "Incident 2: Service Selector Misconfiguration",
                    "desc": "• Symptom: Upstream Ingress returning 503; kubectl get endpoints reported <none>.\n• Root Cause Analysis: Inspected service selector (app: misconfigured-label) vs. active pod labels (app: broken-image).\n• Resolution: Executed kubectl patch service broken-service updating selector to match running pod labels.\n• Result: Endpoints immediately populated with pod IP:port; traffic restored.",
                    "color": ACCENT_PURPLE
                }
            ],
            "notes": (
                "A core competency of a DevOps engineer is troubleshooting live cluster failures. In Session 21, we resolved two critical failure scenarios: "
                "First, an ImagePullBackOff error caused by a typo in the registry repository tag. We investigated using kubectl describe, identified the faulty image URI, and patched the deployment to restore normal operations. "
                "Second, a broken service reporting zero endpoints. By analyzing the service's selector labels against the pod's template labels, we detected the mismatch, patched the service manifest, and verified that endpoint routing was immediately restored."
            )
        },
        {
            "tag": "OBSERVABILITY & SRE",
            "title": "Observability: Telemetry, Metrics & SRE Dashboards",
            "subtitle": "Continuous visibility into application performance and infrastructure health",
            "type": "cards_3",
            "cards": [
                {
                    "title": "Prometheus Instrumentation",
                    "desc": "• FastAPI middleware automatically exports metrics at /metrics\n• Prometheus server scrapes metrics via ServiceMonitor\n• Tracks standard RED metrics: Rate, Errors, and Duration\n• Target health continuously verified in Prometheus Target dashboard",
                    "color": ACCENT_CYAN
                },
                {
                    "title": "Grafana Production Dashboards",
                    "desc": "• HTTP Request Throughput (req/sec by endpoint)\n• p95 / p99 Request Latency distribution\n• HTTP Status Code breakdown (2xx vs 4xx vs 5xx)\n• CPU and Memory utilization per Kubernetes pod",
                    "color": ACCENT_PURPLE
                },
                {
                    "title": "SRE Verification Under Load",
                    "desc": "• Load testing script generates sustained synthetic traffic\n• Validated live Grafana dashboard metric updates\n• Monitored HPA scale-up event from 2 to 4 pods as CPU crossed 60%\n• Confirmed zero dropped requests during auto-scaling events",
                    "color": ACCENT_GREEN
                }
            ],
            "notes": (
                "Observability completes the DevOps loop. Our backend is instrumented with Prometheus client middleware exposing /metrics. "
                "Prometheus scrapes these endpoints, and Grafana visualizes the key RED metrics: Request Rate, Error Rate, and Duration. "
                "During our load testing, we watched real-time traffic spikes trigger Horizontal Pod Autoscaling, verifying that our application dynamically responds to traffic surges without degrading user experience."
            )
        },
        {
            "tag": "SUMMARY & EVALUATION",
            "title": "Project Summary & Key Engineering Takeaways",
            "subtitle": "100/100 Evaluation Alignment Across All 10 Course Modules",
            "type": "split",
            "cards": [
                {
                    "title": "Rubric Module Highlights (M1 - M10)",
                    "desc": "✓ M1-M2: Full-stack CRUD + Automated Pytest coverage\n✓ M3-M4: Clean Git history + Non-root multi-stage Dockerfiles\n✓ M5-M6: GitHub Actions CI/CD + Trivy DevSecOps scanning\n✓ M7-M8: Terraform AWS VPC/EKS + Helm chart orchestration\n✓ M9-M10: Prometheus/Grafana observability + Complete documentation",
                    "color": ACCENT_GREEN
                },
                {
                    "title": "Core Engineering Principles Mastered",
                    "desc": "• Shift-Left Security: Block CVEs before images reach registry\n• Immutable Deployments: Commit SHA tagging eliminates drift\n• Declarative GitOps: Cluster state defined strictly in Git\n• Resilience & Self-Healing: Probes, HPA, and decoupled state",
                    "color": ACCENT_CYAN
                }
            ],
            "notes": (
                "In summary, TaskBoard satisfies every requirement of the 100-point Capstone rubric. "
                "More importantly, it demonstrates core cloud-native engineering principles: shifting security left, using immutable container tags, "
                "managing infrastructure through code, and designing self-healing, observable systems. "
                "Thank you for your time, and I am now happy to take any questions!"
            )
        }
    ]

    def add_header(slide, tag_text, title_text, subtitle_text):
        # Tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_tag = tb_tag.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_CYAN

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.7))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_PRIMARY

        # Subtitle
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.7), Inches(0.45))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = TEXT_MUTED

    for s_idx, data in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)

        # Set background
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = BG_COLOR
        bg_shape.line.fill.background()

        # Add speaker notes
        if "notes" in data and data["notes"]:
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = data["notes"]

        if data["type"] == "title":
            # Title Slide Layout
            # Top Tag
            tb_tag = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(0.5))
            tf_tag = tb_tag.text_frame
            p_tag = tf_tag.paragraphs[0]
            p_tag.text = data["tag"]
            p_tag.font.size = Pt(13)
            p_tag.font.bold = True
            p_tag.font.color.rgb = ACCENT_CYAN

            # Big Title
            tb_title = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(1.2))
            tf_title = tb_title.text_frame
            tf_title.word_wrap = True
            p_title = tf_title.paragraphs[0]
            p_title.text = data["title"]
            p_title.font.size = Pt(36)
            p_title.font.bold = True
            p_title.font.color.rgb = TEXT_PRIMARY

            # Subtitle
            tb_sub = slide.shapes.add_textbox(Inches(1.0), Inches(2.9), Inches(11.3), Inches(0.8))
            tf_sub = tb_sub.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = data["subtitle"]
            p_sub.font.size = Pt(16)
            p_sub.font.color.rgb = TEXT_MUTED

            # 4 Hero Cards
            card_width = Inches(2.65)
            card_height = Inches(2.6)
            card_y = Inches(4.1)
            gap = Inches(0.24)
            start_x = Inches(1.0)

            for i, c in enumerate(data["cards"]):
                cx = start_x + i * (card_width + gap)
                card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_width, card_height)
                card_shape.fill.solid()
                card_shape.fill.fore_color.rgb = CARD_BG
                card_shape.line.color.rgb = c["color"]
                card_shape.line.width = Pt(1.5)

                tf_card = card_shape.text_frame
                tf_card.word_wrap = True
                tf_card.margin_left = Inches(0.2)
                tf_card.margin_right = Inches(0.2)
                tf_card.margin_top = Inches(0.25)
                tf_card.margin_bottom = Inches(0.2)

                p1 = tf_card.paragraphs[0]
                p1.text = c["title"]
                p1.font.size = Pt(15)
                p1.font.bold = True
                p1.font.color.rgb = c["color"]

                p2 = tf_card.add_paragraph()
                p2.text = c["desc"]
                p2.font.size = Pt(12)
                p2.font.color.rgb = TEXT_PRIMARY

        elif data["type"] == "split":
            add_header(slide, data["tag"], data["title"], data["subtitle"])
            cards = data["cards"]
            num_cards = len(cards)

            if num_cards == 2:
                # 2 wide cards side by side
                card_w = Inches(5.7)
                card_h = Inches(4.7)
                card_y = Inches(2.15)
                for i, c in enumerate(cards):
                    cx = Inches(0.8) + i * (card_w + Inches(0.33))
                    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
                    card.fill.solid()
                    card.fill.fore_color.rgb = CARD_BG
                    card.line.color.rgb = c["color"]
                    card.line.width = Pt(1.5)

                    tf = card.text_frame
                    tf.word_wrap = True
                    tf.margin_left = Inches(0.3)
                    tf.margin_right = Inches(0.3)
                    tf.margin_top = Inches(0.3)
                    tf.margin_bottom = Inches(0.3)

                    p1 = tf.paragraphs[0]
                    p1.text = c["title"]
                    p1.font.size = Pt(18)
                    p1.font.bold = True
                    p1.font.color.rgb = c["color"]

                    for line in c["desc"].split("\n"):
                        p = tf.add_paragraph()
                        p.text = line
                        p.font.size = Pt(13)
                        p.font.color.rgb = TEXT_PRIMARY
            else:
                # 2x2 grid
                card_w = Inches(5.7)
                card_h = Inches(2.25)
                for i, c in enumerate(cards):
                    col = i % 2
                    row = i // 2
                    cx = Inches(0.8) + col * (card_w + Inches(0.33))
                    cy = Inches(2.15) + row * (card_h + Inches(0.2))

                    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, card_w, card_h)
                    card.fill.solid()
                    card.fill.fore_color.rgb = CARD_BG
                    card.line.color.rgb = c["color"]
                    card.line.width = Pt(1.2)

                    tf = card.text_frame
                    tf.word_wrap = True
                    tf.margin_left = Inches(0.25)
                    tf.margin_right = Inches(0.25)
                    tf.margin_top = Inches(0.2)
                    tf.margin_bottom = Inches(0.2)

                    p1 = tf.paragraphs[0]
                    p1.text = c["title"]
                    p1.font.size = Pt(15)
                    p1.font.bold = True
                    p1.font.color.rgb = c["color"]

                    for line in c["desc"].split("\n"):
                        p = tf.add_paragraph()
                        p.text = line
                        p.font.size = Pt(11.5)
                        p.font.color.rgb = TEXT_PRIMARY

        elif data["type"] == "cards_3":
            add_header(slide, data["tag"], data["title"], data["subtitle"])
            cards = data["cards"]
            card_w = Inches(3.75)
            card_h = Inches(4.7)
            card_y = Inches(2.15)
            gap = Inches(0.24)

            for i, c in enumerate(cards):
                cx = Inches(0.8) + i * (card_w + gap)
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
                card.fill.solid()
                card.fill.fore_color.rgb = CARD_BG
                card.line.color.rgb = c["color"]
                card.line.width = Pt(1.5)

                tf = card.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.25)
                tf.margin_right = Inches(0.25)
                tf.margin_top = Inches(0.3)
                tf.margin_bottom = Inches(0.3)

                p1 = tf.paragraphs[0]
                p1.text = c["title"]
                p1.font.size = Pt(17)
                p1.font.bold = True
                p1.font.color.rgb = c["color"]

                for line in c["desc"].split("\n"):
                    p = tf.add_paragraph()
                    p.text = line
                    p.font.size = Pt(12)
                    p.font.color.rgb = TEXT_PRIMARY

        # Footer on all slides except title
        if data["type"] != "title":
            tb_footer = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.35))
            tf_footer = tb_footer.text_frame
            p_f = tf_footer.paragraphs[0]
            p_f.text = f"DevOps Capstone (Session 21) • TaskBoard DevSecOps Platform • Slide {s_idx + 1} of {len(slides_data)}"
            p_f.font.size = Pt(9.5)
            p_f.font.color.rgb = RGBColor(100, 116, 139)

    output_path = "/home/dhruv/Projects/Dev/DevOps/Dev-Ops-Shananigans/Capstone-Project/presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

if __name__ == "__main__":
    create_deck()
