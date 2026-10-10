# 02. AWS EC2 (Elastic Compute Cloud)

## 1. What is EC2?
Amazon Elastic Compute Cloud (Amazon EC2) provides scalable virtual servers (instances) in the AWS Cloud. It eliminates the need to invest in hardware up front, enabling fast deployment and scaling of applications.

## 2. Core Concepts
- **AMI (Amazon Machine Image):** A template that contains the software configuration (operating system, application server, applications) required to launch your instance.
- **Instance Types:** Varying combinations of CPU, memory, storage, and networking capacity optimized for specific workloads (e.g., General Purpose `t3`/`m5`, Compute Optimized `c5`, Memory Optimized `r5`).
- **Key Pairs:** Consists of a public key that AWS stores and a private key file that you store. Used to authenticate securely to Linux instances via SSH.
- **Security Groups:** Act as a virtual firewall for your EC2 instances to control incoming (inbound) and outgoing (outbound) traffic at the instance level.
- **EBS (Elastic Block Store):** High-performance block-storage volumes designed for use with EC2 for both throughput and transaction-intensive workloads.
- **Public vs Private IP:**
  - *Public IP:* Reachable from the internet; assigned to instances in public subnets.
  - *Private IP:* Reachable only within the VPC; retained for the lifetime of the instance.
- **Instance Lifecycle:** `Pending` ➔ `Running` ➔ `Stopping` ➔ `Stopped` ➔ `Shutting-down` ➔ `Terminated`.

## 3. Common Use Cases
- Hosting web applications and microservices.
- Running batch processing jobs and CI/CD build runners.
- Hosting database servers with custom storage engines.
