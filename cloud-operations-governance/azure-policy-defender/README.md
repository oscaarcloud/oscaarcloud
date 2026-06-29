# 🧪 Hands-on Lab: Azure Policy + Defender for Cloud Governance Baseline

### Why this matters (Cloud Security)
In cloud environments, security is not only about protecting workloads after deployment. It also depends on enforcing **preventive governance controls** before misconfigurations happen.

In banking or regulated sectors, applying **Azure Policy** for tagging and regional restrictions helps improve **standardization, accountability, and deployment control**, while **Microsoft Defender for Cloud** provides baseline visibility into the security posture of the environment.

---
### Objectives
- Create a governed Resource Group in Azure
- Apply a consistent tagging strategy
- Enforce required tags on Resource Groups using Azure Policy
- Restrict allowed deployment regions using Azure Policy
- Validate subscription-level compliance
- Review baseline posture visibility in Microsoft Defender for Cloud
- Confirm that governance controls are applied successfully

---
### Environment
- Cloud Provider: Microsoft Azure
- Region: East US
- Scope: Azure subscription
- Primary Services:
    - Azure Policy
    - Microsoft Defender for Cloud
- Governance Controls:
    - Required tags on Resource Groups
    - Allowed locations policy


---
### Lab Steps (Summary)
1. Create a **Resource Group**
2. Apply governance tags:
    - `Project`
    - `Environment`
    - `Owner`
    - `Industry`
    - `Purpose`
3. Create Azure Policy assignments to require tags on Resource Groups
4. Create an Azure Policy assignment to restrict deployments to:
    - `East US`
5. Review **Policy Compliance**
6. Review **Microsoft Defender for Cloud Overview**
7. Review **Microsoft Defender for Cloud Recommendations**
8. Validate that all configured policies are compliant

---
### Evidence (Screenshots)
| Step | Screenshot |
|------|------------|
| Resource Group overview | ![](./screenshots/01-resource-group-overview.jpg) |
| Resource Group tags | ![](./screenshots/02-resource-group-tags.jpg) |
| Policy assignment: require Project tag | ![](./screenshots/03-policy-require-project-tag.jpg) |
| Policy assignment: allowed locations | ![](./screenshots/04-policy-allowed-locations.jpg) |
| Policy Compliance overview | ![](./screenshots/05-policy-compliance-overview.jpg) |
| Defender for Cloud overview | ![](./screenshots/06-defender-overview.jpg) |
| Defender for Cloud recommendations | ![](./screenshots/07-defender-recommendations.jpg) |

---
### Resource Group Created
```text
Resource Group: rg-bank-arch-lab
```
- Region: East US
- Used as the governed target for tagging and policy validation

---
### Tagging Strategy
The following tags were applied to the Resource Group:
- Project = PolicyDefenderLab
- Environment = Lab
- Owner = OscarGarcia
- Industry = Banking
- Purpose = GovernanceAndCompliance

> This improves governance consistency, ownership visibility, and operational clarity.

---
### Compliance Validation
Azure Policy Compliance was reviewed after all assignments were created.

**Result**
- All configured policy assignments showed Compliant
- Subscription-level compliance reached 100%
- No non-compliant policies were reported

**This confirmed that:**
- required tags were correctly applied
- governance controls were active
- the regional restriction policy was successfully assigned

---
### Key Takeaways
- Azure Policy is useful for enforcing governance controls before deployment issues happen
- Required tags improve resource visibility, ownership tracking, and standardization
- Allowed location policies help reduce deployment sprawl and support regional governance
- Policy Compliance gives measurable evidence that controls are working
- Defender for Cloud provides posture visibility, even if low-resource labs do not generate many findings
- Governance-first controls are highly relevant for banking and regulated cloud environments