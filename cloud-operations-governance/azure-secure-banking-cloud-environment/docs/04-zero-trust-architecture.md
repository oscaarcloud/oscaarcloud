# Zero Trust Architecture

### Overview

This project uses a Zero Trust approach to design a secure Azure environment for a simulated financial institution.

The architecture follows three main principles:

- Verify explicitly
- Use least privilege access
- Assume breach

### Architecture Diagram

![Architecture Overview](../diagrams/network-segmentation-diagram.png)

### Architecture Components

| Component | Purpose |
|-----------|---------|
| Microsoft Entra ID | Identity and access management |
| Azure Portal | Management access |
| Resource Group | Logical container for project resources |
| Virtual Network | Network isolation and segmentation |
| Subnets | Separation of management, workload, database, and monitoring layers |
| Network Security Groups | Traffic filtering and attack surface reduction |
| Linux VM | Main workload server |
| Azure Policy | Governance and compliance controls |
| Microsoft Defender for Cloud | Security posture management |
| Activity Log | Azure control-plane activity review |
| Log Analytics Workspace | Centralized monitoring and log collection |

### Zero Trust Design Decisions

#### Verify Explicitly

Administrative access is controlled through Microsoft Entra ID, Azure RBAC, and trusted network sources.

#### Least Privilege

Users are separated by roles and assigned only the permissions needed for their responsibilities.

#### Assume Breach

The environment uses segmentation, NSG restrictions, monitoring, Fail2ban, rate limiting, and incident response documentation to reduce impact if a compromise occurs.