# 🧪Hands-on Lab: Windows Update (Patch Management)

### Why this matters (Security)
Keeping systems up to date is a core control for **reducing exposure to known vulnerabilities** and maintaining strong **security hygiene**.  
In banking/regulated environments, patching supports **risk reduction, compliance readiness, and incident prevention**.

---

### Objectives
- Review Windows Update options and update status
- Check for available updates
- Validate installed updates via Update History (KB tracking)
- Verify installed hotfixes via PowerShell

---

### Environment
- Hypervisor: **VMware Workstation**
- OS: **Windows Server 2022**

---

### Lab Steps (Summary)
1. Open **Settings → Update & Security → Windows Update**
2. Review update status and configuration options (Active hours, Advanced options)
3. Click **Check for updates**
4. Monitor download/install status
5. Open **View update history** and confirm installed KBs
6. Verify hotfixes with PowerShell (see command below)

---

### Evidence (Screenshots)
| Step | Screenshot |
|------|------------|
| Windows Update status (updates available / downloading) | ![](./screenshots/01-windows-update-status.jpg) |
| Update history (before) | ![](./screenshots/02-update-history-before.jpg) |
| Windows is up to date | ![](./screenshots/03-windows-update-up-to-date.jpg) |
| Update history (after) | ![](./screenshots/04-update-history-after.jpg) |
| Hotfix verification (PowerShell) | ![](./screenshots/05-hotfix-verification-powershell.jpg) |

---

### Command used for Hotfix verification
```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 15
```

---

### Key Takeaways
- Patch management reduces exposure to known vulnerabilities.
- KB history provides audit-friendly traceability (useful for compliance and troubleshooting).
- Maintenance windows help apply updates without disrupting operations.