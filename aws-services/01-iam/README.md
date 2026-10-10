# 01. AWS IAM (Identity and Access Management)

## 1. What is IAM?
AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

## 2. Core IAM Components
- **Users:** An entity that you create in AWS to represent a person or application that needs to interact with AWS (has long-term credentials like passwords or access keys).
- **Groups:** A collection of IAM users. Groups let you specify permissions for multiple users, making permissions easier to manage.
- **Roles:** An IAM identity that you can create in your account that has specific permissions, but is not associated with a specific person. It is assumed temporarily by users, applications, or AWS services (like EC2 or Lambda).
- **Policies:** An object in AWS that, when associated with an identity or resource, defines their permissions (JSON format: Effect, Action, Resource).
- **Permissions:** Declarations defining what actions are allowed or denied on specific AWS resources.

## 3. Principles & Best Practices
- **Principle of Least Privilege:** Grant only the permissions required to perform a specific task, and no more.
- **MFA (Multi-Factor Authentication):** Enforce MFA on root and all privileged user accounts.
- **Avoid Root User Usage:** Lock away root credentials and use IAM identities for daily tasks.
- **Use Roles for Applications & EC2:** Never hardcode AWS access keys in code or on EC2 instances; use IAM Roles instead.

## 4. Common Use Cases
- Delegating cross-account access securely without sharing API keys.
- Giving EC2 instances automatic, temporary permissions to read from an S3 bucket via Instance Profiles.
- Enforcing fine-grained department-level permissions (e.g. Developers vs DevOps vs Finance).
