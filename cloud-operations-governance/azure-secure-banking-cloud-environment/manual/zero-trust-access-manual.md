# Zero Trust Access Manual

### Purpose

This manual defines how access should be managed in the NovaBank Azure environment using Zero Trust principles.

### Core Principles

- Verify explicitly
- Use least privilege access
- Assume breach

### Access Rules

- Administrative access must be restricted to trusted sources.
- Users must only receive the permissions required for their role.
- Direct public access to management ports is not allowed.
- MFA is required for administrative users in production.
- Access reviews should be performed monthly.

### Recommended Improvements

- Conditional Access
- Privileged Identity Management
- Azure Bastion
- Microsoft Sentinel