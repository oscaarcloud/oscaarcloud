# ☁️ Cloud Security

This section contains hands-on labs focused on securing cloud environments, primarily in Azure.

The work here is centered on identity, access control, secure configurations, and visibility across cloud resources, with scenarios aligned to **banking and regulated environments**.

---

### What You’ll Find Here

- Identity & Access Management (IAM / RBAC)
- Resource access control
- Secure cloud configurations
- Logging and monitoring
- Secrets management

---

### Lab Focus

These labs are designed to reflect how cloud resources are secured in environments where:

- access must be tightly controlled
- actions must be traceable
- sensitive information must be protected
- cloud configurations must follow security best practices

---

### Environment Context

All labs are approached with a **banking and regulated environment mindset**, where identity boundaries, auditability, and secure access are critical.

Work is developed and tested in **controlled environments** to keep implementations safe, reproducible, and practical.

---

### Current Direction

This section is being built around Azure-based security implementations such as:

- IAM / RBAC
- secure access to resources
- monitoring and visibility
- secrets protection

---

### Available Labs

- **[Azure VM deployment with secure SSH access](./azure-vm-secure-ssh/README.md)**
Secure Azure VM deployment with SSH hardening, NSG restrictions, and firewall validation.

- **[Azure Policy + Defender for Cloud Governance Baseline](./azure-policy-defender/README.md)**
Governance baseline with Azure Policy tag enforcement, regional restrictions, and Defender for Cloud visibility.

- **[Azure Key Vault + Managed Identity for Internal Banking App Configuration](./azure-key-vault/README.md)**
  Secure secret management pattern using Azure Key Vault, Managed Identity, RBAC, and Azure App Service for an internal banking-style application.

- **[Azure Bastion Secure VM Access](./azure-bastion-secure-vm-access/README.md)**
Secure administrative access to a private Azure Linux VM using Azure Bastion, without public IP exposure or open inbound SSH ports.

- **[Azure Landing Zone Secure Baseline](./azure-landing-zone-secure-baseline/README.md)**
Secure Azure foundation with Resource Group organization, governance tags, VNet subnet segmentation, NSG baseline, and Azure Policy enforcement.