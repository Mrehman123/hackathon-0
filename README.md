# Personal AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This is a **Bronze Tier** implementation of the Personal AI Employee Hackathon 2026. It provides the foundational layer for an autonomous AI agent that manages your personal and business affairs using Qwen Code and Obsidian.

## 🏆 Bronze Tier Deliverables (Complete)

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (File System Monitoring)
- ✅ Qwen Code integration for reading/writing to the vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ All AI functionality implemented as Agent Skills

## 📁 Project Structure

```
hackathon-0/
├── AI_Employee_Vault/       # Obsidian vault (your AI's memory)
│   ├── Dashboard.md         # Main status dashboard
│   ├── Company_Handbook.md  # Rules and guidelines
│   ├── Business_Goals.md    # Business objectives
│   ├── Inbox/               # Raw incoming items
│   ├── Needs_Action/        # Items requiring processing
│   ├── Plans/               # Multi-step task plans
│   ├── Pending_Approval/    # Awaiting human approval
│   ├── Approved/            # Approved for action
│   ├── Rejected/            # Rejected items
│   ├── Done/                # Completed tasks
│   ├── Logs/                # Action logs
│   ├── Briefings/           # CEO briefings
│   ├── Accounting/          # Financial records
│   └── Invoices/            # Generated invoices
├── scripts/
│   ├── base_watcher.py      # Base class for all watchers
│   ├── filesystem_watcher.py # File system watcher (Bronze Tier)
│   ├── orchestrator.py      # Main orchestration process
│   └── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

1. **Qwen Code** - Install from Qwen Code
   ```bash
   npm install -g @anthropic/qwen-code
   ```

2. **Python 3.10+** - Download from [python.org](https://python.org/downloads/)

3. **Obsidian** - Download from [obsidian.md](https://obsidian.md/download)

### Installation

1. **Install Python dependencies**:
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

2. **Open the vault in Obsidian**:
   - Open Obsidian
   - Click "Open folder as vault"
   - Select the `AI_Employee_Vault` folder

3. **Verify Qwen Code works**:
   ```bash
   qwen --version
   ```

### Running the AI Employee

#### Option 1: Start the Orchestrator (Recommended)

The orchestrator continuously monitors the Needs_Action folder and processes files:

```bash
cd scripts
python orchestrator.py ../AI_Employee_Vault
```

#### Option 2: Start the File System Watcher

The watcher monitors a drop folder for new files:

```bash
cd scripts
python filesystem_watcher.py ../AI_Employee_Vault
```

This creates a `Drop` folder inside `AI_Employee_Vault/Inbox/`. Any files you copy there will be automatically processed.

#### Option 3: Manual Qwen Processing

Process files manually with Qwen:

```bash
cd AI_Employee_Vault
qwen "Check /Needs_Action folder and process all pending items"
```

## 📖 How It Works

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   File Drop     │────▶│  File Watcher    │────▶│  Needs_Action   │
│   (User)        │     │  (Python)        │     │  (Folder)       │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Dashboard     │◀────│  Claude Code     │◀────│  Orchestrator   │
│   (Update)      │     │  (Reasoning)     │     │  (Python)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Workflow

1. **Drop a file** into `AI_Employee_Vault/Inbox/Drop/`
2. **Filesystem Watcher** detects the new file
3. **Watcher** copies file to vault and creates action file in `Needs_Action/`
4. **Orchestrator** detects action file and triggers Qwen Code
5. **Qwen** reads Company_Handbook.md for rules
6. **Qwen** processes the file and takes appropriate action
7. **Qwen** updates Dashboard.md and logs the action
8. **File** is moved to `Done/` folder

## 📝 Usage Examples

### Example 1: Process a Document

1. Drop a PDF or text file into `AI_Employee_Vault/Inbox/Drop/`
2. The watcher creates an action file automatically
3. Claude processes it according to the Company Handbook
4. Check `Dashboard.md` for the results

### Example 2: Manual Task Assignment

Create a file in `Needs_Action/`:

```markdown
---
type: task
source: manual
priority: high
status: pending
---

# Task: Review Q1 Budget

Please review the Business_Goals.md and create a summary of:
1. Current revenue vs target
2. Any subscriptions that need auditing
3. Recommendations for cost optimization
```

Then run:
```bash
python orchestrator.py ../AI_Employee_Vault
```

### Example 3: Check Status

```bash
cd AI_Employee_Vault
qwen "What items are pending in /Needs_Action? Summarize the current state."
```

## 🎯 Company Handbook Rules

The AI Employee follows these key rules:

| Action | Auto-Approve | Require Approval |
|--------|--------------|------------------|
| File processing | ✅ All | ❌ Never |
| Payments | < $50 recurring | > $100 or new payee |
| Emails | Known contacts | New contacts |
| File delete | ❌ Never | ✅ Always |

**Priority Keywords**: urgent, asap, invoice, payment, help, emergency, deadline

## 🔧 Configuration

### Customize Company Handbook

Edit `AI_Employee_Vault/Company_Handbook.md` to:
- Change approval thresholds
- Add custom rules
- Define business-specific workflows

### Customize Business Goals

Edit `AI_Employee_Vault/Business_Goals.md` to:
- Set revenue targets
- Define key metrics
- Track active projects

## 📊 Monitoring

### Check Logs

Logs are stored in `AI_Employee_Vault/Logs/YYYY-MM-DD.md`:

```bash
cat AI_Employee_Vault/Logs/2026-03-31.md
```

### View Dashboard

Open `AI_Employee_Vault/Dashboard.md` in Obsidian for real-time status.

### Check Processed Items

```bash
ls AI_Employee_Vault/Done/
```

## 🛠️ Troubleshooting

### Qwen Code not found

```bash
npm install -g @anthropic/qwen-code
```

### Watcher not detecting files

1. Ensure the watcher is running
2. Check that files have `.md` extension (for action files)
3. Verify the Drop folder path is correct

### Orchestrator not processing files

1. Check that Qwen Code is installed and working
2. Verify the vault path is correct
3. Check logs for error messages

### Python import errors

```bash
cd scripts
pip install -r requirements.txt
```

## 📚 Next Steps (Silver Tier)

To upgrade to Silver Tier, add:

1. **Gmail Watcher** - Monitor Gmail for new messages
2. **WhatsApp Watcher** - Monitor WhatsApp Web
3. **MCP Server** - Send emails automatically
4. **Approval Workflow** - Human-in-the-loop for sensitive actions
5. **Scheduled Tasks** - Cron jobs for daily briefings

## 📄 License

This project is part of the Personal AI Employee Hackathon 2026.

## 🤝 Contributing

Share your improvements with the community! Join the Wednesday Research Meeting:

- **When**: Wednesdays at 10:00 PM
- **Zoom**: [https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **YouTube**: [https://www.youtube.com/@panaversity](https://www.youtube.com/@panaversity)

## 📞 Support

- **Documentation**: See `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Skill Documentation**: See `.qwen/skills/ai-employee-vault-ops/SKILL.md`

---

*Built for the Personal AI Employee Hackathon 2026 - Bronze Tier Complete ✅*
