# Public Exposure Response Playbook

### Scenario

A virtual machine or administrative service was found exposed to the Internet.

This can happen when SSH, RDP, database ports, or other sensitive services are allowed from `0.0.0.0/0` or from the `Internet` service tag without proper restrictions.


---
### Severity

High


---
### Examples

- SSH open to the Internet.
- RDP open to the Internet.
- Database port exposed publicly.
- Public IP assigned to a resource unnecessarily.
- NSG rule allowing `Any` source to administrative ports.
- Temporary access rule left enabled after maintenance.


---
### Possible Impact

- Brute-force attacks.
- Unauthorized administrative access.
- Credential compromise.
- Lateral movement.
- Data exposure.
- Increased attack surface.
- Higher risk of automated scanning and exploitation.


---
### Detection Sources

- NSG inbound rules.
- VM networking configuration.
- Resource Group resource list.
- Azure Resource Visualizer.
- Azure Policy compliance.
- Linux authentication logs.
- Nginx access logs if the exposed service is web-based.


---
### Response Steps

1. Identify the exposed resource.
2. Review the VM networking configuration.
3. Review NSG inbound rules.
4. Identify any rule allowing access from `0.0.0.0/0`, `Any`, or `Internet`.
5. Remove unnecessary public access.
6. Restrict required access to a trusted IP.
7. Validate that the service is still reachable only from approved sources.
8. Check authentication logs for suspicious activity.
9. Document the exposure and evidence collected.
10. Recommend Azure Bastion for production environments.


---
### Azure Portal Checks

| Area | What to Review |
|---|---|
| VM Networking | Confirm which inbound ports are allowed. |
| NSG Rules | Check if SSH, RDP, or other sensitive ports are exposed to the Internet. |
| Public IP | Confirm whether the VM requires a public IP address. |
| Resource Visualizer | Review the relationship between VM, NIC, Public IP, VNet, and NSGs. |
| Azure Policy | Check if any governance policy can prevent this exposure. |


---
### Useful Commands

| Command | Purpose |
|---|---|
| `sudo tail -n 50 /var/log/auth.log` | Reviews recent authentication activity on the Linux VM. |
| `sudo grep "Failed password" /var/log/auth.log` | Searches for failed SSH login attempts. |
| `sudo systemctl status ssh` | Confirms whether the SSH service is running. |
| `sudo fail2ban-client status sshd` | Checks whether Fail2ban is monitoring and blocking suspicious SSH attempts. |


---
### Evidence to Collect

- VM networking screenshot.
- NSG inbound rules screenshot.
- Public IP configuration screenshot.
- Resource visualizer screenshot.
- Authentication log screenshot if suspicious activity is found.
- Fail2ban SSH jail status screenshot if SSH brute-force attempts are detected.


---
### Preventive Controls

- Restrict SSH access to a trusted IP.
- Deny SSH from the Internet.
- Avoid exposing RDP publicly.
- Avoid assigning public IP addresses unless required.
- Use Azure Bastion in production.
- Use SSH key-based authentication.
- Disable password-based SSH login.
- Review NSG rules regularly.
- Remove temporary access rules after use.