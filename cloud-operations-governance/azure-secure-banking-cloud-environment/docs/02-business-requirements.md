# Business Requirements

### Overview

NovaBank Financial Services needs a secure Azure environment to support a small internal banking workload. The environment must be simple enough for a lab subscription but realistic enough to demonstrate cloud security engineering practices.

### Requirements

| ID | Requirement | Description |
|---|---|---|
| BR-01 | Secure Cloud Foundation | The environment must be deployed inside a dedicated Azure Resource Group. |
| BR-02 | Network Segmentation | The network must be separated into management, workload, database, and monitoring subnets. |
| BR-03 | Controlled Administrative Access | SSH or RDP access must not be openly exposed to the Internet. |
| BR-04 | Least Privilege | Users must receive only the permissions required for their role. |
| BR-05 | Governance | Resources must follow naming and tagging standards. |
| BR-06 | Monitoring | Security posture and activity logs must be reviewed. |
| BR-07 | Attack Prevention | The environment must include controls against brute-force attacks and excessive login requests. |
| BR-08 | Incident Response | The project must include basic incident response playbooks. |
| BR-09 | Documentation | All implementation steps, evidence, and limitations must be documented. |

### Business Value

This project helps demonstrate how a cloud security engineer can design a secure cloud baseline for a regulated environment such as banking or financial services.