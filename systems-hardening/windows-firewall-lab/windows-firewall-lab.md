# 🧪 Hands-on Lab: Windows Firewall with Advanced Security

### Why this matters (Security)

Windows Defender Firewall is a critical defensive security control used to filter inbound and outbound network traffic. Proper firewall configuration reduces the attack surface of a system and helps prevent unauthorized access, malware communication, and service exposure.

In enterprise and banking environments, firewall rules help enforce network segmentation, protect sensitive services, and ensure that only authorized traffic is allowed.

---

### Objectives

By completing this lab, the following security tasks are demonstrated:

- Review Windows Firewall configuration
- Configure inbound firewall rules
- Configure outbound firewall rules
- Control traffic using ports and applications
- Apply network profile–based security policies
- Validate firewall rule configuration

---

### Environment

Hypervisor: VMware Workstation  
Operating System: Windows Server 2022  
Security Tool: Windows Defender Firewall with Advanced Security

---

### Lab Scenarios

This lab demonstrates several practical firewall configurations used in enterprise environments.

Scenario 1: Block Remote Desktop on the Public Network (Inbound Rule)

Scenario 2: Block Outbound Traffic for a Specific Application

Scenario 3: Block Web Server (HTTP) Traffic on a Public Network

Scenario 4: Allow Key Management Service on Domain/Private networks and deny Public access

---

### Evidence (Screenshots)

### Scenario 1 — Block Remote Desktop on Public Network (Inbound Rules)

| Step | Screenshot |
|-----|------------|
| Select **Port** rule type when creating a new inbound firewall rule. | ![](./screenshot/scenario1/scenario1-rule-type.jpg) |
| Configure the rule to block **TCP port 3389**, which is used by Remote Desktop Protocol (RDP). | ![](./screenshot/scenario1/scenario1-rdp-port.jpg) |
| Set the firewall rule action to **Block the connection**. | ![](./screenshot/scenario1/scenario1-block-action.jpg) |
| Apply the rule only to the **Public network profile**. | ![](./screenshot/scenario1/scenario1-public-profile.jpg) |
| Name the rule **Block Remote Desktop on Public Network**. | ![](./screenshot/scenario1/scenario1-rule-name.jpg) |
| Verify the rule appears in the **Inbound Rules list**. | ![](./screenshot/scenario1/scenario1-rule-created.jpg) |

---

### Scenario 2 — Block Outbound Traffic for a Specific Application (Outbound Rules)

| Step | Screenshot |
|-----|------------|
| Create a new outbound rule using the **Program rule type**. | ![](./screenshot/scenario2/scenario2-rule-type.jpg) |
| Select the executable file for **Microsoft Edge (msedge.exe)**. | ![](./screenshot/scenario2/scenario2-program-path.jpg) |
| Configure the action to **Block the connection**. | ![](./screenshot/scenario2/scenario2-block-action.jpg) |
| Apply the rule to **Domain, Private, and Public network profiles**. | ![](./screenshot/scenario2/scenario2-profile.jpg) |
| Verify the rule appears as **Block Edge Internet Access** in the outbound rules list. | ![](./screenshot/scenario2/scenario2-rule-created.jpg) |

---

### Scenario 3 — Block HTTP Traffic on Public Network (Inbound Rules)

| Step | Screenshot |
|-----|------------|
| Create a new inbound rule using the **Port rule type**. | ![](./screenshot/scenario3/scenario3-rule-type.jpg) |
| Configure the rule to block **TCP port 80**, which is used for HTTP web traffic. | ![](./screenshot/scenario3/scenario3-http-port.jpg) |
| Set the rule action to **Block the connection**. | ![](./screenshot/scenario3/scenario3-block-action.jpg) |
| Apply the rule only to the **Public network profile**. | ![](./screenshot/scenario3/scenario3-public-name.jpg) |
| Name the rule **Block HTTP on Public Network**. | ![](./screenshot/scenario3/scenario3-rule-name.jpg) |
| Verify the rule appears in the firewall rules list. | ![](./screenshot/scenario3/scenario3-rule-created.jpg) |

---

### Scenario 4 — Configure Key Management Service (KMS) Access

| Step | Screenshot |
|-----|------------|
| Locate the **Key Management Service (TCP-In)** rule in the inbound rules list. | ![](./screenshot/scenario4/scenario4-kms-rule.jpg) |
| Open the rule properties to review the configuration. | ![](./screenshot/scenario4/scenario4-kms-properties.jpg) |
| Configure the rule to allow connections on **Domain and Private networks**. | ![](./screenshot/scenario4/scenario-kms-domain-private.jpg) |
| Disable or block the rule for the **Public network profile**. | ![](./screenshot/scenario4/scenario4-kms-public-block.jpg) |
| Verify the final rule configuration in the firewall rules list. | ![](./screenshot/scenario4/scenario4-kms-final.jpg) |

---

### Key Security Takeaways

Firewall rules are a fundamental part of system hardening and network security.

Key lessons demonstrated in this lab:

- Blocking **RDP (TCP 3389)** on public networks helps prevent unauthorized remote access attempts.
- Outbound firewall rules can prevent **applications from communicating with external servers**.
- Blocking **HTTP traffic (TCP 80)** helps avoid exposing unintended services on public networks.
- Network profiles (Domain, Private, Public) allow administrators to apply **different security policies depending on the network environment**.
- Internal services such as **Key Management Service (KMS)** should only be accessible from trusted networks.
