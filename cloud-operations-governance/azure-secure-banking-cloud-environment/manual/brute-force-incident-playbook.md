# Brute Force Incident Response Playbook

### Scenario

Multiple failed SSH login attempts were detected against a Linux virtual machine.


---
### Severity

High


---
### Possible Impact

- Unauthorized access
- Credential compromise
- Service disruption
- Lateral movement
- Increased exposure of administrative services


---
### Detection Sources

- `/var/log/auth.log`
- `/var/log/fail2ban.log`
- Fail2ban status
- NSG rule review
- VM networking configuration


---
### Response Steps

1. Identify the source IP address.
2. Review failed authentication logs.
3. Check the Fail2ban SSH jail status.
4. Confirm whether Fail2ban blocked the suspicious IP.
5. Restrict NSG rules if SSH is exposed.
6. Disable password-based SSH login if it is enabled.
7. Rotate affected credentials or SSH keys if compromise is suspected.
8. Review administrator accounts.
9. Document evidence.
10. Add preventive controls.


---
### Useful Commands

```bash
sudo grep "Failed password" /var/log/auth.log       # Searches for failed SSH login attempts in the authentication log.
sudo tail -n 50 /var/log/auth.log                   # Displays the last 50 authentication log entries to review recent login activity.
sudo tail -n 50 /var/log/fail2ban.log               # Displays the last 50 Fail2ban log entries to check bans, warnings, or service activity.
sudo fail2ban-client status                         # Shows the general Fail2ban status and active jails.
sudo fail2ban-client status sshd                    # Shows detailed status for the SSH jail, including failed attempts and banned IPs.
sudo systemctl status fail2ban --no-pager           # Checks whether the Fail2ban service is running correctly.
sudo grep -E "PermitRootLogin|PubkeyAuthentication|PasswordAuthentication|MaxAuthTries|AllowUsers" /etc/ssh/sshd_config     # Reviews the main SSH hardening settings configured on the server.
```


---
### Evidence to Collect
- Failed login logs
- Fail2ban status screenshot
- Fail2ban SSH jail status screenshot
- NSG inbound rule screenshot
- VM networking screenshot
- SSH hardening configuration screenshot


---
### Preventive Controls
- Use SSH key-based authentication.
- Disable password-based SSH login.
- Disable root login.
- Restrict SSH access to a trusted IP.
- Use Fail2ban to block repeated failed attempts.
- Review NSG rules regularly.
- Use Azure Bastion in production environments.