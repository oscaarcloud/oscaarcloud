# 🧪 Hands-on Lab: DNS Filtering with Windows Defender Firewall

### Why this matters
Controlling outbound network traffic is an important security practice in enterprise environments. By restricting DNS requests through Windows Defender Firewall, administrators can limit how systems resolve external domains and better control network communication.

In production environments, outbound filtering can help reduce unnecessary exposure, enforce network policies, and strengthen endpoint security by limiting unauthorized or unwanted traffic.

---
### Objectives
- Access the **Windows Defender Firewall** interface
- Create a new **outbound rule**
- Block **DNS traffic** using port `53`
- Verify that the rule was created successfully

---
### Environment
- Platform: Windows
- Security Tool: Windows Defender Firewall
- Rule Direction: Outbound
- Rule Type: Port
- Protocol: UDP
- Remote Port: `53`
- Action: Block the connection
- Profiles: Domain, Private, Public
- Rule Name: `DNS Filter`

---
### Lab Steps (Summary)
1. Open **Windows Defender Firewall with Advanced Security**
2. Go to **Outbound Rules**
3. Select **New Rule**
4. Choose **Port**
5. Select **UDP**
6. Configure **Specific remote ports: 53**
7. Select **Block the connection**
8. Apply the rule to:
    - `Domain`
    - `Private`
    - `Public`
9. Name the rule **DNS Filter**
10. Finish the wizard
11. Verify that the rule appears in **Outbound Rules**

---
### Evidence (Screenshots)
| Step | Screenshot |
|------|------------|
| Rule type: Port | ![](./screenshots/01-rule-type-port.jpg) |
| UDP port 53 configured | ![](./screenshots/02-udp-port-53.jpg) |
| Block the connection | ![](./screenshots/03-block-connection.jpg) |
| Profiles selected | ![](./screenshots/04-profiles-selected.jpg) |
| Rule name: DNS Filter | ![](./screenshots/05-rule-name-dns-filter.jpg) |
| DNS Filter rule visible | ![](./screenshots/06-rule-name-dns-filter-visible.jpg) |

---
### Firewall Rule Configuration
- **Direction:** Outbound
- **Type:** Port
- **Protocol:** UDP
- **Remote Port:** `53`
- **Action:** Block the connection
- **Profiles:** Domain, Private, Public
- **Rule Name:** `DNS Filter`

>This rule blocks outbound DNS requests, preventing the system from resolving domain names through standard DNS queries.

---
### Key Takeaways
- Windows Defender Firewall can be used to control outbound traffic, not only inbound traffic
- Blocking DNS requests is a useful way to restrict domain resolution
- Outbound filtering helps enforce network security policies
- Rule validation is important to confirm that the configuration was applied correctly
- Firewall rule management is a practical part of Windows security hardening