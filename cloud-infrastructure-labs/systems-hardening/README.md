# 🖥️ Systems Hardening

This section contains hands-on labs focused on securing operating systems and enforcing stronger system-level protections.

The work here covers both Linux and Windows, with emphasis on access control, secure configuration, and hardening practices that reduce attack surface.

---

### What You’ll Find Here

- Linux hardening
- Windows security configurations
- User and group management
- File permission controls
- SSH security
- Access control enforcement
- CIS-aligned practices

---

### Lab Focus

These labs are designed to reflect system security work such as:

- enforcing least privilege
- strengthening system access controls
- securing services and configurations
- reducing exposure through hardening measures

---

### Environment Context

All work is structured with **banking and regulated environments** in mind, where system integrity, access restrictions, and secure baselines are critical.

Labs are developed and tested in **controlled environments** using virtual machines and isolated setups.

---

### Current Direction

This section is currently focused on:

- Linux (RHEL) hardening
- Windows endpoint security
- access control
- secure system configuration

---

### Available Labs

- **[Windows Defender Hardening](./windows-defender-lab/README.md)**  
  Endpoint protection configuration, real-time scanning, and malware detection validation.

- **[Windows Firewall Hardening](./windows-firewall-lab/README.md)**  
  Inbound/outbound traffic control, port filtering, and network profile enforcement.

- **[Password Policy Enforcement](./windows-password-policy-lab/README.md)**  
  Local Group Policy configuration for strong password requirements and account security.

- **[Windows Update Management](./windows-update-lab/README.md)**  
  Patch management validation and system update verification using Windows Update.

- **[DHCP Server Configuration](./dhcp-server-configuration/README.md)**
  DHCP role deployment, IPv4 scope creation, exclusion range configuration, and lease management on Windows Server.

- **[DNS Filtering](./dns-filtering/README.md)**
  Outbound firewall rule creation to restrict DNS traffic and strengthen network traffic control in Windows.

- **[Secure Web Server Deployment on RHEL](./rhel-secure-web-server/README.md)**
Security-conscious RHEL web server deployment with SSH hardening, SELinux validation, firewalld restrictions, Nginx service validation, logging review, and Chrony time synchronization.