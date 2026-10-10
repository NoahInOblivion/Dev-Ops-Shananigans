# 05. AWS DynamoDB & RDS (Database Services)

## Part A: Amazon DynamoDB (NoSQL)

### 1. What is DynamoDB?
Amazon DynamoDB is a fully managed, serverless, key-value and document NoSQL database designed for single-digit millisecond performance at any scale.

### 2. Core Concepts
- **Tables:** A collection of data items (similar to a table in SQL or a collection in MongoDB).
- **Items:** A group of attributes that is uniquely identifiable among all other items (similar to a row).
- **Attributes:** A fundamental data element (similar to a column or field).
- **Primary Keys:**
  - *Partition Key (Hash Key):* Used by DynamoDB's internal hash function to distribute items across partitions.
  - *Sort Key (Range Key):* Used to sort items that share the same partition key.
- **Use Cases:** Real-time gaming leaderboards, shopping carts, session management, IoT sensor feeds.

---

## Part B: Amazon RDS (Relational Database Service)

### 1. What is RDS?
Amazon Relational Database Service (Amazon RDS) is a managed relational database service that automates time-consuming administration tasks such as hardware provisioning, database setup, patching, and backups.

### 2. Core Concepts
- **Supported Engines:** PostgreSQL, MySQL, MariaDB, Oracle Database, Microsoft SQL Server, Amazon Aurora.
- **DB Instances:** The basic building block of Amazon RDS; an isolated database environment in the cloud.
- **Security:** Network isolation via VPC private subnets, encryption at rest using AWS KMS, and SSL/TLS encryption in transit.
- **Backups:** Automated daily snapshots and transaction logs enabling point-in-time recovery (PITR) up to 35 days.
- **Multi-AZ Deployments:** Synchronous replication to a standby instance in a different Availability Zone for high availability and automatic failover.
- **Read Replicas:** Asynchronous replication to offload read-heavy database workloads and scale read throughput horizontally.
- **Use Cases:** E-commerce transactions, financial reporting systems, enterprise CRM and ERP platforms.
