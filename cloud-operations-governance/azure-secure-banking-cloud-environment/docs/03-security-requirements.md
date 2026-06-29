# Security Requirements

### Overview

The security requirements are based on Zero Trust principles: verify explicitly, use least privilege, and assume breach.

### Requirements

| ID | Security Requirement | Control |
|---|---|---|
| SR-01 | Administrative access must be restricted | NSG rules, trusted IP, Bastion recommended |
| SR-02 | Users must follow least privilege | Microsoft Entra ID groups and Azure RBAC |
| SR-03 | Network traffic must be segmented | VNet, subnets, NSGs |
| SR-04 | SSH brute-force risk must be reduced | Fail2ban, SSH hardening, NSG restrictions |
| SR-05 | Login abuse must be reduced | Nginx rate limiting for `/login` |
| SR-06 | Public exposure must be minimized | No unnecessary public access |
| SR-07 | Insecure configurations must be detected | Azure Policy and Defender for Cloud |
| SR-08 | Security events must be reviewed | Activity Log, Linux logs, Nginx logs |
| SR-09 | Incident response must be documented | Security playbooks |
| SR-10 | Secrets must not be stored in GitHub | Key Vault recommended, no secrets in repo |

### Zero Trust Mapping

| Zero Trust Principle | Applied Control |
|---|---|
| Verify Explicitly | Entra ID, trusted IP, MFA recommended |
| Least Privilege | RBAC, groups, limited permissions |
| Assume Breach | Segmentation, monitoring, Fail2ban, playbooks |