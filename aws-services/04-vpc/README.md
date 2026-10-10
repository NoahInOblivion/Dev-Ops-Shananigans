# 04. AWS VPC (Virtual Private Cloud)

## 1. What is VPC?
Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual network that you've defined, giving you complete control over your virtual networking environment.

## 2. Core Concepts
- **CIDR (Classless Inter-Domain Routing):** The IP address range assigned to the VPC (e.g., `10.0.0.0/16`).
- **Subnets:** A range of IP addresses in your VPC located within a single Availability Zone.
  - *Public Subnet:* Has a route to the Internet Gateway; instances receive public IPs.
  - *Private Subnet:* Has no direct route to the Internet Gateway; used for secure databases and backend services.
- **Route Tables:** A set of rules (routes) used to determine where network traffic from your subnet or gateway is directed.
- **Internet Gateway (IGW):** A horizontally scaled, redundant VPC component that allows communication between your VPC and the internet.
- **NAT Gateway:** Enables instances in a private subnet to connect to the internet or other AWS services, while preventing the internet from initiating a connection with those instances.
- **Security Groups vs Network ACLs (NACLs):**
  - *Security Group:* Stateful firewall operating at the EC2 instance level.
  - *NACL:* Stateless firewall operating at the subnet boundary level (supports explicit Allow and Deny rules).

## 3. Common Use Cases
- Multi-tier web applications (public frontend, private application servers, private database).
- Hybrid cloud architectures extending on-premises networks to AWS via VPN or Direct Connect.
