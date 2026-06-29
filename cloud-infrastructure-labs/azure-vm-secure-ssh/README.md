# 🧪 Hands-on Lab: Azure VM Deployment with Secure SSH Access

### Why this matters (Cloud Security)
Deploying virtual machines securely in cloud environments is a fundamental skill for cloud engineers and system administrators.

In production environments (especially banking or regulated sectors), controlling access via **Network Security Groups (NSG)**, validating connectivity, and ensuring proper network segmentation are critical for **reducing attack surface and maintaining compliance**.

---
### Objectives
- Deploy a Linux Virtual Machine in Azure
- Configure Virtual Network and Subnets
- Implement secure access using NSG (restrict SSH to a specific IP)
- Validate connectivity via SSH
- Verify internal network configuration
- Ensure basic host-level security (UFW firewall)
- Confirm SSH service status

---
### Environment
- Cloud Provider: Microsoft Azure
- Region: East US
- OS: Ubuntu 24.04 LTS
- Access Method: SSH (Key-based authentication)
- Security Controls:
    - Network Security Group (NSG)
    - Linux Firewall (UFW)

---
### Lab Steps (Summary)
1. Create a **Resource Group**
2. Deploy a **Virtual Network (VNet)** with two subnets:
    - `snet-management`
    - `snet-backend`
3. Deploy a **Linux Virtual Machine**
4. Assign:
    - Public IP (for SSH access)
    - Private IP (internal communication)
5. Create an **NSG rule**:
    - Allow SSH (port 22)
    - Restrict access to a specific public IP
6. Connect to the VM using SSH
7. Validate system configuration:
    - whoami
    - hostname
    - ip a
8. Verify firewall (UFW) status
9. Validate SSH service (`systemctl status ssh`)
10. Clean up resources by deleting the resource group

---

### Evidence (Screenshots)
| Step | Screenshot |
|------|------------|
| Architecture diagram | ![](./screenshots/architecture.jpg) |
| VM Overview | ![](./screenshots/vm-overview.jpg) |
| Subnets configuration | ![](./screenshots/subnets.jpg) |
| VM Networking | ![](./screenshots/vm-networking.jpg) |
| NSG rule (SSH restricted) | ![](./screenshots/nsg-ssh-rule.jpg) |
| SSH successful connection | ![](./screenshots/ssh-success.jpg) |
| VM validation (whoami, hostname, ip a) | ![](./screenshots/vm-validation.jpg) |
| UFW  firewall active | ![](./screenshots/ufw-active.jpg) |
| SSH service running | ![](./screenshots/ssh-service-running.jpg) |

---
### SSH Access — Command Used
```bash
ssh -i "vm-corebank-01_key.pem" azureadmin@<public-ip>
```
- Key-based authentication used
- Secure remote access validated

---
### NSG Rule Configuration
- Port: 22
- Protocol: TCP
- Source: Specific IP only
- Destination: VM subnet
- Action: Allow

>This ensures SSH access is restricted, preventing unauthorized connections.

---
### Validation Commands
```bash
whoami                      # Shows the current logged-in user
hostname                    # Displays the VM hostname
ip a                        # Displays network interfaces and assigned IP addresses
sudo ufw status             # Verifies that the UFW firewall is active and show allowed rules
sudo systemctl status ssh   # Confirms that the SSH service is running correctly
```

---
### Validation Commands
All resource were removed by deleting:
```
Resource Group: rg-bank-arch-lab
```
- Prevents unnecessary cloud costs
- Ensures clean enviroment after testing

---
### Key Takeaways
- NSG rules are critical to restrict inbound access and reduce exposure
- SSH access should always be limited to trusted IP addresses
- Validating connectivity ensures correct network configuration
- UFW adds an extra layer of host-based protection
- Verifying services (`systemctl`) is essential for troubleshooting
- Proper cleanup is part of real-world cloud operations