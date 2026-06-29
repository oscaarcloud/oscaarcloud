# Cloud Misconfiguration Response Playbook

### Scenario

A cloud resource was created without required tags or with an insecure configuration.

This type of issue can happen when resources are deployed quickly without following governance, naming, tagging, or security standards.


---
### Severity

Low to Medium

Severity may increase to High if the misconfiguration exposes sensitive resources to the Internet or allows unauthorized access.


---
### Examples

- Resource created without required tags.
- Resource deployed in the wrong Azure region.
- SSH or RDP opened to the Internet.
- NSG rule configured with overly permissive access.
- Public IP assigned unnecessarily.
- Resource created outside the approved naming convention.
- Azure Policy compliance failure.


---
### Possible Impact

- Lack of ownership visibility.
- Poor cost tracking.
- Compliance gaps.
- Increased attack surface.
- Unauthorized access risk.
- Difficulty during audits.
- Uncontrolled resource growth.


---
### Detection Sources

- Azure Policy compliance.
- Resource Group review.
- Resource tags.
- NSG inbound rules.
- VM networking configuration.
- Cost analysis.
- Manual configuration review.


---
### Response Steps

1. Identify the affected resource.
2. Review the resource configuration.
3. Check Azure Policy compliance.
4. Confirm whether required tags are missing.
5. Review NSG rules if the issue is network-related.
6. Apply missing tags.
7. Correct insecure configuration.
8. Validate that the resource follows the project standard.
9. Review whether an Azure Policy assignment should prevent the issue in the future.
10. Document the issue and evidence collected.


---
### Azure Portal Checks

| Area | What to Review |
|---|---|
| Resource Group | Confirm the resource is inside `rg-novabank-secure-env`. |
| Tags | Verify required tags such as `Project`, `Environment`, `Owner`, and `Department`. |
| NSG Rules | Check if any rule allows unnecessary public access. |
| VM Networking | Confirm SSH is restricted to a trusted IP. |
| Azure Policy | Review policy assignments and compliance results. |
| Cost Analysis | Check whether the resource is increasing lab cost unexpectedly. |


---
### Evidence to Collect

- Resource configuration screenshot.
- Tags screenshot.
- Azure Policy compliance screenshot.
- NSG inbound rules screenshot.
- VM networking screenshot if applicable.
- Cost analysis screenshot if the issue affects cost visibility.


---
### Preventive Controls

- Use Azure Policy to require tags.
- Use Azure Policy to restrict allowed locations.
- Review NSG rules before deployment.
- Follow naming conventions.
- Apply least privilege access.
- Review resources regularly.
- Delete unused resources after the lab.