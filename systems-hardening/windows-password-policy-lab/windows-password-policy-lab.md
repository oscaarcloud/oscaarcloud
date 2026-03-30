# 🧪 Hands-on Lab: Enforce Strong Password Policies

### Why this matters (Security)

Password policies are a foundational access control in any regulated environment. In banking and financial institutions, enforcing strong password requirements reduces the risk of unauthorized access through brute-force or credential-based attacks. Configuring and documenting these controls supports **compliance readiness** (e.g., PCI-DSS, ISO 27001, NIST) and demonstrates a proactive security posture aligned with endpoint hardening standards.

---

### Objectives

- Check password strength using Kaspersky's password checker
- Review the Windows Local Group Policy Editor (`gpedit`)
- Configure password policies based on Microsoft recommendations:
  - Enforce password history
  - Maximum password age
  - Minimum password age
  - Minimum password length
- Verify applied policies via `net accounts` and `gpupdate /force`

---

### Environment

- **Hypervisor:** VMware Workstation
- **OS:** Windows Server 2022
- **Tool:** Windows Local Group Policy Editor (`gpedit.msc`)
- **External validator:** [password.kaspersky.com](https://password.kaspersky.com)

---

### Lab Steps (Summary)

1. Open Chrome and navigate to `password.kaspersky.com`
2. Test weak password: `fido1973` (letters + numbers, common word + birth year)
3. Test moderate password: `Fido1973!` (8 chars, uppercase, number, symbol)
4. Test strong password: `Mh1llifwwas!` (12 chars, passphrase-based, mixed complexity)
5. Open Command Prompt and run `gpedit` to launch the Local Group Policy Editor
6. Navigate to: `Computer Configuration → Windows Settings → Security Settings → Account Policies → Password Policy`
7. Configure the following policies:

| Policy | Before | Configured Value | Microsoft Recommendation |
|---|---|---|---|
| Enforce password history | 0 passwords remembered | 24 passwords | 24 |
| Maximum password age | 42 days | 60 days | 30–90 days |
| Minimum password age | 0 days | 1 day | 1 day |
| Minimum password length | 0 characters | 12 characters | 8–14 characters |

---

### Evidence (Screenshots)
| Step | Screenshot |
|------|------------|
| Password Policy — Before Configuration | ![](./screenshots/01-password-policy-before.jpg) |
| Password Policy — After Configuration | ![](./screenshots/02-password-policy-after.jpg) |
| Verification — `net accounts` | ![](./screenshots/03-net-accounts-verification.jpg) |
| Verification — `gpupdate /force` | ![](./screenshots/04-gpupdated-force.jpg) |

---

### Policy Descriptions Reference

| Policy | Purpose |
|---|---|
| **Enforce password history** | Prevents reuse of recent passwords. Ensures users don't cycle back to old credentials. |
| **Maximum password age** | Forces periodic password rotation to limit exposure window from compromised credentials. |
| **Minimum password age** | Prevents users from immediately changing back to a previous password, enforcing history policy effectiveness. |
| **Minimum password length** | Increases entropy and brute-force resistance. Longer passwords are exponentially harder to crack. |
| **Password must meet complexity requirements** | Requires uppercase, lowercase, digits, and symbols — already **Enabled** by default in this environment. |
| **Store passwords using reversible encryption** | Remains **Disabled** — reversible storage is equivalent to plaintext and a critical vulnerability. |

---

### Key Takeaways

- **Weak passwords based on personal info** (names, birth years) are highly vulnerable to brute-force and dictionary attacks, regardless of basic number substitution.
- **Passphrase-based passwords** (first letters of a memorable sentence) achieve strong entropy while remaining user-friendly — length matters more than complexity alone.
- **Group Policy enforcement** removes reliance on user discipline; controls are applied system-wide and are audit-traceable.
- **`net accounts`** provides CLI-level verification of applied password policies — useful for scripted audits and compliance checks.
- **`gpupdate /force`** ensures policies are applied immediately without waiting for the default refresh interval, which is critical in incident response or audit scenarios.
- Documenting Group Policy configurations supports **audit readiness** and demonstrates control implementation for frameworks like PCI-DSS, NIST 800-53, and ISO 27001.
