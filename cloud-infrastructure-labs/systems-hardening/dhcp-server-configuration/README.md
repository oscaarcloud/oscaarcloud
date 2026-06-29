# 🧪 Hands-on Lab: Installing and Configuring DHCP on Windows Server

### Why this matters
Dynamic Host Configuration Protocol (DHCP) is a core network service that automates IP address assignment in enterprise networks.

In production environments, properly configuring DHCP helps reduce manual configuration errors, prevent IP conflicts, improve operational efficiency, and maintain better control over internal network infrastructure. It is especially important when some assets, such as printers or servers, require static IP addresses and must be excluded from the dynamic allocation pool.

---
### Objectives
- Install the **DHCP Server** role
- Complete **post-installation DHCP configuration**
- Create an **IPv4 scope**
- Configure an IP range from **192.168.1.2 to 192.168.1.254**
- Add **exclusion ranges** for devices using static IP addresses
- Configure the **lease duration**
- Activate the scope

---
### Environment
- Platform: Windows Server
- Service: DHCP Server
- Network Type: Local Area Network (LAN)
- Scope Name: `companyLAN`
- IPv4 Range: `192.168.1.2 - 192.168.1.254`
- Lease Duration: `1 day`

---
### Lab Steps (Summary)
1. Open **Server Manager**
2. Start the **Add Roles and Features Wizard**
3. Select and install the **DHCP Server** role
4. Add the required features
5. Complete the **post-installation configuration**
6. Create the DHCP administrative security groups
7. Open **DHCP Manager**
8. Start the **New Scope Wizard**
9. Create the scope named **companyLAN**
10. Configure the address pool:
    - Start IP: `192.168.1.2`
    - End IP: `192.168.1.254`
11. Add exclusion ranges:
    - `192.168.1.30 - 192.168.1.32`
    - `192.168.1.40 - 192.168.1.41`
    - `192.168.1.56`
12. Set the lease duration to **1 day**
13. Activate the scope
14. Verify that the scope appears as **active**

---
### Evidence (Screenshots)

#### Task A — Installation
| Step | Screenshot |
|------|------------|
| DHCP role selected | ![](./screenshots/TaskA/03-dhcp-role-selected.jpg) |
| Required features added | ![](./screenshots/TaskA/04-add-features.jpg) |
| Installation successful | ![](./screenshots/TaskA/05-installation-successful.jpg) |
| Post-installation configuration | ![](./screenshots/TaskA/06-post-install-coonfig.jpg) |
| DHCP post-install wizard | ![](./screenshots/TaskA/07-dhcp-post-install-wizard.jpg) |
| DHCP groups created | ![](./screenshots/TaskA/08-dhcp-groups-created.jpg) |

#### Task B — Scope Configuration
| Step | Screenshot |
|------|------------|
| DHCP Manager | ![](./screenshots/TaskB/08-dhcp-manager.jpg) |
| New Scope Wizard | ![](./screenshots/TaskB/09-new-scope-wizard.jpg) |
| Scope name configured | ![](./screenshots/TaskB/10-scope-name-companylan.jpg) |
| IPv4 range configured | ![](./screenshots/TaskB/11-ipv4-range-configured.jpg) |
| Exclusion ranges | ![](./screenshots/TaskB/13-exclusion-ranges.jpg) |
| Lease duration | ![](./screenshots/TaskB/14-lease-duration.jpg) |
| Scope activation | ![](./screenshots/TaskB/16-scope-activation.jpg) |
| Final active scope | ![](./screenshots/TaskB/17-final-active-scope.jpg) |
---
### Scope Configuration
- **Scope Name:** `companyLAN`
- **Address Pool:** `192.168.1.2 - 192.168.1.254`
- **Exclusion Ranges:**
    - `192.168.1.30 - 192.168.1.32`
    - `192.168.1.40 - 192.168.1.41`
    - `192.168.1.56`
- **Lease Duration:** `1 day`
- **Default Gateway:** Not configured in this lab
- **DNS:** Not configured in this lab
- **WINS:** Not configured in this lab
- **Status:** Active

>This configuration allows DHCP to dynamically assign IP addresses to client devices while preventing conflicts with systems that already use static IP addresses.

---
### Key Takeaways
- DHCP simplifies IP address management in enterprise networks
- Exclusion ranges help prevent conflicts with statically assigned devices
- Post-installation configuration is required to complete DHCP deployment
- Proper scope design improves network organization and reliability
- Core infrastructure services like DHCP are important for daily network operations