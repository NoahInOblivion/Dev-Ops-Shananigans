# 03. AWS S3 (Simple Storage Service)

## 1. What is S3?
Amazon S3 is an object storage service offering industry-leading scalability, data availability, security, and performance. S3 stores data as objects within buckets.

## 2. Core Concepts
- **Buckets:** Top-level containers for objects. Bucket names must be globally unique across all AWS accounts worldwide.
- **Objects:** The fundamental entities stored in S3, consisting of object data (file content) and metadata (key-value pairs describing the object).
- **Storage Classes:**
  - *S3 Standard:* For frequently accessed data with low latency.
  - *S3 Intelligent-Tiering:* Automatically moves objects between access tiers based on changing patterns.
  - *S3 Standard-IA:* For infrequent access with rapid retrieval.
  - *S3 Glacier Flexible / Deep Archive:* Low-cost archival for compliance and long-term retention.
- **Versioning:** Keeps multiple variants of an object in the same bucket to protect against accidental deletes and overwrites.
- **Lifecycle Policies:** Automatic rules to transition objects to cheaper storage classes or permanently delete them after an expiration period.
- **Encryption:** Server-Side Encryption (SSE-S3, SSE-KMS, SSE-C) and Client-Side Encryption for data at rest.
- **Bucket Policies:** JSON-based access control policies attached directly to S3 buckets specifying allowed principals and actions.

## 3. Common Use Cases
- Static website hosting (HTML, CSS, JS).
- Backup and disaster recovery storage.
- Data lakes for analytics and machine learning.
