# Scenario Overview

### Project Name & Organization

Azure Secure Banking Cloud Environment | NovaBank Financial Services

### Scenario

NovaBank Financial Services is a simulated financial institution that is migrating a small internal workload to Microsoft Azure.

Because the environment may handle sensitive business information, the cloud infrastructure must be designed with security controls from the beginning. The goal is to build a secure Azure baseline using Zero Trust principles, network segmentation, least privilege access, governance policies, monitoring, and incident response documentation.

### Business Context

The company needs a secure cloud environment where administrators can manage resources, security analysts can review security posture, developers can access only the resources they need, and auditors can review the environment without making changes.

The environment must reduce the risk of public exposure, brute-force attacks, excessive login requests, privilege misuse, insecure configurations, and lack of visibility.

### Role

Cloud Security Engineer

### Main Goal

Design and implement a secure Azure cloud environment for a simulated financial institution using Azure Portal and security best practices.

### Scope

This project includes:

- Azure Resource Group
- Virtual Network and subnets
- Network Security Groups
- Linux virtual machine
- SSH hardening
- Fail2ban
- Nginx rate limiting
- Microsoft Entra ID users and groups
- Azure RBAC
- Azure Policy
- Microsoft Defender for Cloud
- Azure Activity Log
- Security documentation
- Incident response playbooks

### Out of Scope

The following controls are documented as recommended production improvements but may not be fully implemented due to lab subscription limitations:

- Azure Bastion
- Azure Web Application Firewall
- Azure DDoS Protection
- Microsoft Sentinel
- Advanced Conditional Access
- Privileged Identity Management
- Production database deployment