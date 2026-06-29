# Security Operations Manual

### Purpose
This manual defines the security operations process for the NovaBank Azure lab environment.

The goal is to provide a simple and repeatable process to review security controls, validate configurations, monitor basic logs, and respond to possible security issues.

This manual focuses on the controls implemented in the lab, including NSG rule review, SSH hardening, Nginx log review, Fail2ban monitoring, Azure Policy review, and cost visibility.


---
### Security Monitoring Scope
The security review process covers the following areas:

- Network Security Group inbound rules
- SSH access configuration
- Linux authentication logs
- Nginx service and access logs
- Nginx rate limiting configuration
- Fail2ban SSH protection
- Azure Policy assignments
- Resource tags
- Cost analysis
- VM networking configuration

The following services are recommended for production environments but were not fully implemented in this lab:

- Microsoft Defender for Cloud
- Azure Activity Log monitoring and alerting
- Log Analytics Workspace
- Microsoft Sentinel


---
### Microsoft Defender for Cloud Review
Microsoft Defender for Cloud should be used in production environments to review cloud security posture, recommendations, and workload protection.

In this lab, Defender for Cloud is documented as a recommended future improvement.

Recommended review items:

- Secure Score
- Security recommendations
- Regulatory compliance
- Public exposure recommendations
- VM security recommendations
- Network security recommendations

Production recommendation:
```text
Enable Microsoft Defender for Cloud to continuously assess the Azure environment and provide security posture recommendations.
```


---
### Secure Score Review
Secure Score helps measure the security posture of the Azure environment.

In a production environment, the security team should review Secure Score regularly and prioritize recommendations based on risk.

Recommended review process:

1. Open Microsoft Defender for Cloud.
2. Review Secure Score.
3. Identify high-impact recommendations.
4. Prioritize recommendations related to identity, network, and workload security.
5. Document changes made to improve the score.

For this lab, Secure Score is listed as a recommended improvement because the main focus was on manual implementation of security controls.


---
### NSG Rule Review
Network Security Groups are one of the main security controls in this project.

The goal of the NSG review is to confirm that only required traffic is allowed and administrative access is not exposed to the Internet.

Review these NSGs:
| NSG | Purpose |
|-----|---------|
|`nsg-management`| Controls administrative access |
|`nsg-workload`| Controls web workload access |
|`nsg-database`| Protects the simulated database subnet |
|`nsg-monitoring`| Protects the monitoring subnet |

Review checklist:
- Confirm SSH is not open to the entire Internet.
- Confirm SSH is restricted to a trusted IP.
- Confirm HTTP/HTTPS rules are intentional.
- Confirm database ports are not exposed to the Internet.
- Confirm deny rules are in place where needed.
- Confirm temporary rules are removed when no longer needed.

Important rules to review:
| Rule | Purpose |
|------|---------|
|`Allow-SSH-Trusted-IP-Temp`| Allows SSH only from a trusted public IP |
|`Deny-SSH-Internet`| Blocks SSH access from the Internet |
|`Allow-HTTP`| Allows web traffic to the workload |
|`Allow-HTTPS| Allows secure web traffic to the workload |


---
### Identity Access Review
Identity access review ensures that users and roles follow the principle of least privilege.

In this lab, identity access was designed conceptually using Microsoft Entra ID and Azure RBAC.

Recommended role model:
|        Role         |        Access Level          |
|---------------------|------------------------------|
| Cloud Administrator |        Contributor           |
|  Security Analyst   |	  Security Reader / Reader   |
|      Developer      | Limited Contributor / Reader |
|       Auditor       |           Reader             |

Review checklist:
- Avoid assigning Owner unless required.
- Assign permissions at the Resource Group level when possible.
- Review administrative users regularly.
- Remove unused accounts.
- Require MFA for administrative users in production.
- Use Conditional Access in production.

Production recommendations:
- Microsoft Entra MFA
- Conditional Access
- Privileged Identity Management
- Access reviews


---
### Azure Activity Log Review
Azure Activity Log should be used to review control-plane activity in Azure.

This includes resource creation, deletion, policy assignments, NSG rule changes, and VM updates.

In this lab, Activity Log is documented as a recommended monitoring control.

Recommended events to review:
- Resource creation
- Resource deletion
- Network Security Group rule changes
- Policy assignment changes
- VM start/stop activity
- Role assignment changes

Recommended response process:

- Identify the event.
- Review who made the change.
- Confirm whether the change was authorized.
- Check the affected resource.
- Document the finding if the change was suspicious.


---
### Linux Authentication Log Review
Linux authentication logs help detect failed login attempts, SSH activity, and possible brute-force attempts.

Main log file:

`/var/log/auth.log`

Useful commands:

| Command | Purpose |
| `sudo tail -n 50 /var/log/auth.log` |	Shows recent authentication activity. |
| `sudo grep "Failed password" /var/log/auth.log` |	Searches for failed SSH login attempts. |
| `sudo grep "Accepted publickey" /var/log/auth.log` | Searches for successful SSH logins using public key authentication. |

Review checklist:

- Look for repeated failed login attempts.
- Check for unknown source IPs.
- Confirm successful logins are expected.
- Review activity after public exposure events.
- Escalate if suspicious login attempts are detected.


---
### Nginx Log Review
Nginx logs help review web traffic, access patterns, and possible endpoint abuse.

Main log files:

```test
/var/log/nginx/access.log
/var/log/nginx/error.log
```

Useful commands:

| Command | Purpose |
| `sudo tail -n 50 /var/log/nginx/access.log` |	Shows recent web requests. |
| `sudo tail -n 50 /var/log/nginx/error.log` | Shows recent Nginx errors. |
| `sudo grep "/login" /var/log/nginx/access.log` |	Searches for requests targeting the /login endpoint. |
| `sudo grep "limiting requests" /var/log/nginx/error.log` |	Searches for rate limiting events if triggered. |

Review checklist:

- Look for repeated requests to `/login`.
- Check for unknown user agents.
- Check for scanning activity.
- Review HTTP status codes.
- Confirm the rate limiting configuration is still present.


---
### Fail2ban Review
Fail2ban is used to reduce the risk of SSH brute-force attacks.

Useful commands:

| Command |	Purpose |
|`sudo systemctl status fail2ban` |	Checks if Fail2ban is running. |
|`sudo fail2ban-client status` |	Shows active Fail2ban jails. |
|`sudo fail2ban-client status sshd` |	Shows SSH jail details, failed attempts, and banned IPs. |
|`sudo cat /etc/fail2ban/jail.d/sshd.local` |	Displays the SSH jail configuration. |
|`sudo fail2ban-server -t` |	Validates the Fail2ban configuration. |

Review checklist:

- Confirm Fail2ban service is active.
- Confirm the sshd jail is enabled.
- Review banned IPs.
- Review failed attempts.
- Confirm configuration values such as maxretry, findtime, and bantime.

Configured values:

|Setting | Value |
|`maxretry` |  `5` |
|`findtime` |  `10m` |
|`bantime`  |  `30m` |
|`backend`  |  `systemd` |


---
### Monthly Security Checklist
Use this checklist to review the environment regularly.

Area	Check
Resource Group	Confirm only expected resources exist.
Tags	Confirm required tags are present.
Cost	Review cost analysis for unexpected charges.
NSG Rules	Confirm SSH is restricted to trusted IP.
VM	Confirm the VM is only running when needed.
SSH	Confirm root login and password authentication are disabled.
Nginx	Confirm the service is running and /login is protected.
Fail2ban	Confirm the sshd jail is active.
Azure Policy	Review policy assignments and compliance.
Documentation	Update README and manuals if changes were made.

---
### Incident Escalation Process
If suspicious activity is detected, follow this process:

Identify the affected resource.
Determine the type of issue:
Brute-force attempt
Web endpoint abuse
Public exposure
Misconfiguration
Review relevant logs or Azure settings.
Apply immediate containment:
Restrict NSG rules
Block suspicious IPs if needed
Disable unnecessary public access
Stop the VM if the risk is high
Collect evidence.
Follow the correct incident response playbook.
Document the incident.
Apply preventive controls.

Relevant playbooks:

Incident Type	Playbook
SSH brute-force attempt	brute-force-incident-playbook.md
Web endpoint abuse	web-attack-response-playbook.md
Public exposure	public-exposure-response-playbook.md
Cloud misconfiguration	misconfiguration-response-playbook.md