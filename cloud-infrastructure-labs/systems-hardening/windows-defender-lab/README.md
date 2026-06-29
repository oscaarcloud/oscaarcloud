# 🧪 Hands-on Lab: Windows Defender (AV Baseline + Scheduled Scan)

### Why this matters (Security)
Microsoft Defender is a core endpoint security control for **malware prevention, detection, and response**.  
In banking/regulated environments, having Defender **enabled, updated, and validated with evidence** supports **security hygiene, audit readiness, and incident prevention**.

---

### Objectives
- Confirm Defender core protections are enabled (Real-time protection)
- Validate Defender is updated (Security intelligence / Protection updates)
- Run an on-demand scan (Quick scan)
- Create a scheduled scan using Task Scheduler (weekly full scan)
- Validate detection visibility using the EICAR test file (Protection history)

---

### Environment
- Hypervisor: **VMware Workstation**
- OS: **Windows Server 2022**
- Security tool: **Microsoft Defender Antivirus**
- Scheduler: **Windows Task Scheduler**

---

### Lab Steps (Summary)
1. Open **Windows Security → Virus & threat protection**
2. Run a **Quick scan** to validate on-demand scanning works
3. Confirm **Real-time protection** is **ON**
4. Check **Protection updates** and confirm Security intelligence is up to date
5. Create a **weekly scheduled scan** using Task Scheduler:
   - General: run whether user is logged on or not + run with highest privileges
   - Trigger: weekly schedule (example: Sundays at 3:00 AM)
   - Action: run `MpCmdRun.exe` with scan arguments
   - Conditions/Settings: wake to run, retries, and allow run on demand
6. Validate the task appears in Task Scheduler and will run on schedule
7. (Validation) Download the **EICAR** test file and confirm Defender logs it in **Protection history**

---

### Evidence (Screenshots)
| Step | Screenshot |
|------|------------|
| Protection updates (Security intelligence up to date) | ![](screenshots/01-protection-updates.jpg) |
| Quick scan running | ![](screenshots/02-quick-scan-running.jpg) |
| Real-time protection ON | ![](screenshots/03-real-time-protection-on.jpg) |
| Task Scheduler — General settings | ![](screenshots/04-task-scheduler-general-settings.jpg) |
| Task Scheduler — Trigger (weekly schedule) | ![](screenshots/05-task-scheduler-trigger(weekly%20schedule).jpg) |
| Task Scheduler — Action (MpCmdRun.exe) | ![](screenshots/06-task-scheduler-action(MpCmdRun.exe).jpg) |
| Task Scheduler — Conditions (AC power + wake) | ![](screenshots/07-task-scheduler-conditions-(AC-power-wake).jpg) |
| Task Scheduler — Settings (retry + on-demand) | ![](screenshots/08-task-scheduler-settings(retry_on-demand).jpg) |
| Task created (visible in Task Scheduler library) | ![](screenshots/09-task-created-and-visible-in-task-scheduler-library.jpg) |
| Protection history showing EICAR detection | ![](screenshots/10-protection-history-showing-EICAR-detection.jpg) |

---

### Defender Scheduled Scan — Commands & Configuration
**Program/script:**
- `C:\ProgramFiles\Windows Defender\MpCmdRun.exe`

**Arguments (example):**
- Quick scan: `-Scan -ScanType 1`
- Full scan: `-Scan -ScanType 2`

> In this lab, the scheduled task was configured for a **weekly Full Scan**.

---

### Key Takeaways
- Defender must be **enabled and up to date** to reduce exposure to commodity malware and known threats.
- Running an **on-demand scan** and confirming **real-time protection** verifies baseline endpoint security posture.
- Scheduling scans via **Task Scheduler + MpCmdRun.exe** ensures consistent hygiene and repeatable controls.
- **Protection history** provides evidence for investigations and audits (visibility into detections and actions taken).
- The **EICAR test file** is a safe way to validate detection and logging without using real malware.