# Administrator Manual

### Purpose
This manual defines how the NovaBank Azure lab environment should be managed from an administrative perspective.

The goal is to keep the environment organized, secure, auditable, and easy to maintain. This manual covers resource naming, tagging, access management, network administration, VM administration, NSG changes, backup considerations, change management, and resource cleanup.


---
### Environment Overview

The NovaBank Azure environment was created as a cloud security capstone project focused on building a secure baseline for a simulated financial institution.

| Area | Value |
|---|---|
| Project Name | Azure Secure Banking Cloud Environment |
| Simulated Organization | NovaBank Financial Services |
| Cloud Provider | Microsoft Azure |
| Main Resource Group | `rg-novabank-secure-env` |
| Region | `East US` |
| Virtual Network | `vnet-novabank-prod` |
| Main VM | `vm-novabank-secure-env` |
| Operating System | Ubuntu Linux |
| Main Security Controls | NSG rules, SSH hardening, Fail2ban, Nginx rate limiting, Azure Policy |

The environment includes a segmented virtual network, dedicated Network Security Groups, a Linux virtual machine, SSH key-based access, Nginx, Fail2ban, and Azure Policy assignments for governance.


---
### Resource Naming Convention
All resources should follow a clear and consistent naming convention. This helps with organization, troubleshooting, documentation, and audit review.

| Resource Type | Naming Format | Example |
|---|---|---|
| Resource Group | `rg-[project]-[purpose]-[env]` | `rg-novabank-secure-env` |
| Virtual Network | `vnet-[project]-[env]` | `vnet-novabank-prod` |
| Subnet | `snet-[purpose]` | `snet-workload` |
| Network Security Group | `nsg-[purpose]` | `nsg-workload` |
| Virtual Machine | `vm-[project]-[purpose]` | `vm-novabank-secure-env` |
| Public IP | `[vm-name]-ip` | `vm-novabank-secure-env-ip` |
| SSH Key | `key-[project]-[purpose]` | `key-novabank-web-01` |
| Policy Assignment | `[control]-[scope]` | `Require Project Tag` |

Recommended naming rules:

- Use lowercase letters when possible.
- Use hyphens instead of spaces.
- Keep names short but descriptive.
- Include the project or workload name.
- Include the resource purpose when possible.
- Avoid random names unless Azure generates them automatically.


---
### Tagging Standard
Tags are used to identify ownership, purpose, environment, compliance context, and cost tracking.

All resources should include the following tags when supported:

| Tag | Value |
|---|---|
| `Environment` | `Lab` |
| `Department` | `Security` |
| `Owner` | `OscarGarcia` |
| `Project` | `NovaBank Cloud Security Capstone` |
| `Compliance` | `NIST-CSF-Aligned` |
| `CostCenter` | `Training` |

#### Why tagging matters

Tagging helps with:

- Resource ownership
- Cost visibility
- Governance
- Compliance tracking
- Resource cleanup
- Environment classification

Resources without required tags should be reviewed and updated.


---
### Access Management

Administrative access must follow the principle of least privilege.

#### Access rules
- Administrative access should only be granted to authorized users.
- SSH access must use key-based authentication.
- Password-based SSH authentication should remain disabled.
- Root login should remain disabled.
- SSH access must be restricted to a trusted public IP using NSG rules.
- Users should not be granted the `Owner` role unless required.
- Access should be reviewed before and after major changes.

#### Recommended role model
| Role | Access Level | Purpose |
|---|---|---|
| Cloud Administrator | Contributor | Manage lab resources |
| Security Analyst | Security Reader / Reader | Review security posture |
| Developer | Limited Contributor / Reader | Access workload resources only |
| Auditor | Reader | Review configuration and evidence |

#### Production recommendations
For a production environment, the following controls should be added:

- Multi-Factor Authentication
- Conditional Access
- Privileged Identity Management
- Azure Bastion
- Just-In-Time VM access


---
### Network Administration
The network is designed using segmentation to reduce exposure and limit lateral movement.

#### Virtual Network

| Resource | Value |
|---|---|
| Virtual Network | `vnet-novabank-prod` |
| Address Space | `10.10.0.0/16` |

#### Subnets
| Subnet | Address Range | Purpose |
|---|---|---|
| `snet-management` | `10.10.1.0/24` | Administrative access |
| `snet-workload` | `10.10.2.0/24` | Linux VM and web workload |
| `snet-database` | `10.10.3.0/24` | Simulated database layer |
| `snet-monitoring` | `10.10.4.0/24` | Monitoring/logging layer |

#### Network administration rules
- Do not expose administrative ports to the entire Internet.
- SSH should only be allowed from a trusted IP.
- HTTP/HTTPS should only be open when required.
- Database traffic should not be allowed directly from the Internet.
- Each subnet should have its own NSG.
- NSG rules should be reviewed before changes are applied.


---
### VM Administration

The main VM is used to host the lab workload and security controls.

| Item | Value |
|---|---|
| VM Name | `vm-novabank-secure-env` |
| OS | Ubuntu Linux |
| Access Method | SSH key |
| Main Services | OpenSSH, Nginx, Fail2ban |

#### VM administration tasks
Administrators should regularly validate:

```bash
whoami
hostnamectl
ip a
uname -a
sudo systemctl status ssh --no-pager
sudo systemctl status nginx --no-pager
sudo systemctl status fail2ban --no-pager
```

#### SSH hardening settings
The SSH configuration should include:
```ssh
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
MaxAuthTries 3
AllowUsers oscaradmin
```
- Validation command: `sudo sshd -t`. If the command returns no error, the SSH configuration syntax is valid.


---
### NSG Change Process
Network Security Group changes must be handled carefully because incorrect rules can expose the environment.

Before changing an NSG rule, document:

- Reason for the change
- Affected NSG
- Affected subnet or resource
- Source
- Destination
- Port
- Protocol
- Action
- Priority
- Security impact
- Rollback plan

#### Example NSG rule change record
| Field | Example |
|-------|---------|
| Change | Allow SSH from trusted IP |
| NSG | `nsg-workload` |
| Source | Trusted public IP |
| Destination | Any |
| Port | 22 |
| Protocol | TCP |
| Action | Allow |
| Priority | 120 |
| Reason | Temporary administrative access |
| Rollback | Remove rule after configuration is complete |

#### NSG rule principles
- Use the lowest required access.
- Avoid Any when a specific source can be used.
- Avoid allowing SSH/RDP from Internet.
- Use deny rules for administrative ports where needed.
- Keep priorities organized and documented.


---
### Backup and Recovery Considerations
This lab environment does not implement a full backup and recovery solution because it was created for learning and demonstration purposes.

However, in a production environment, backup and recovery should include:

- VM backup using Azure Backup
- Configuration backup for Nginx
- Configuration backup for Fail2ban
- SSH key protection
- Recovery plan for deleted resources
- Backup retention policy
- Regular restore testing

#### Important files to back up in production
```text
/etc/ssh/sshd_config
/etc/nginx/nginx.conf
/etc/nginx/sites-available/default
/etc/fail2ban/jail.d/sshd.local
```

#### Lab recovery approach
For this lab, recovery is based on documentation and screenshots. The enviromment can be rebuit using the implementation steps and configuration evidence stored in the repository.


---
### Change Management Process
All changes to the environment should follow a basic change management process.

#### Required information before making a change
- What is being changed?
- Why is the change needed?
- What resource is affected?
- What is the security impact?
- What is the rollback plan?
- Was the change validated?

#### Change workflow
1. Identify the required change.
2. Review possible security impact.
3. Apply the change.
4. Validate the result.
5. Capture evidence if needed.
6. Update documentation.
7. Roll back if the change causes issues.

#### Example validation commands
```bash
sudo nginx -t
sudo sshd -t
sudo fail2ban-server -t
sudo systemctl status nginx --no-pager
sudo systemctl status ssh --no-pager
sudo systemctl status fail2ban --no-pager
```


---
### Decommissioning Process
After the lab is completed and all screenshots/evidence have been collected, resources should be deleted to avoid unnecessary costs.

#### Decommissioning steps
1. Confirm all required screenshtos are saved.
2. Confirm documentation is stored in the repository.
3. Confirm no additional validation is needed.
4. Go to Azure Portal.
5. Open the Resource Group: `rg-novabank-secure-env`
6. Select **Delete resource group**.
7. Type the Resource Group name to confirm deletion.
8. Confirm the deletion.
9. Verify that the resources were removed.

#### Why this matters
Deleting unused lab resources helps prevent unexpected Azure charges and keeps the subscription clean.