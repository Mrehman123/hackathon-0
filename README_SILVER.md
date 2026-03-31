# Personal AI Employee - Silver Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This is the **Silver Tier** implementation of the Personal AI Employee Hackathon 2026. It builds upon the Bronze Tier foundation to add multiple watchers, MCP servers, approval workflows, and scheduled tasks.

## 🏆 Silver Tier Deliverables (Complete)

- ✅ All Bronze Tier requirements
- ✅ **Two or more Watcher scripts** (Gmail + WhatsApp + File System)
- ✅ **LinkedIn auto-posting** (with human approval)
- ✅ **Qwen reasoning loop** that creates Plan.md files
- ✅ **One working MCP server** for external action (Email)
- ✅ **Human-in-the-loop approval workflow** for sensitive actions
- ✅ **Basic scheduling** via Task Scheduler
- ✅ **All AI functionality as Agent Skills**

---

## 📁 Project Structure

```
hackathon-0/
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Business_Goals.md
│   ├── Briefings/              # Daily/Weekly briefings
│   ├── Accounting/             # Financial records
│   ├── Inbox/
│   │   └── Drop/               # File drop folder
│   ├── Needs_Action/           # Items requiring processing
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved for action
│   ├── Rejected/               # Rejected items
│   ├── Done/                   # Completed tasks
│   └── Logs/                   # Action logs
├── scripts/
│   ├── base_watcher.py         # Base class for watchers
│   ├── filesystem_watcher.py   # File system watcher
│   ├── gmail_watcher.py        # Gmail API watcher
│   ├── whatsapp_watcher.py     # WhatsApp Web watcher
│   ├── orchestrator.py         # Main orchestration
│   ├── approval_handler.py     # HITL approval executor
│   ├── scheduler.py            # Scheduled tasks
│   ├── requirements.txt        # Bronze dependencies
│   └── requirements-silver.txt # Silver dependencies
├── mcp-servers/
│   ├── email-mcp/              # Email sending MCP
│   │   ├── email_mcp.js
│   │   └── package.json
│   └── linkedin-mcp/           # LinkedIn posting MCP
│       ├── linkedin_mcp.js
│       └── package.json
├── .qwen/skills/
│   ├── ai-employee-vault-ops/  # Vault operations skill
│   └── ai-employee-silver-tier/ # Silver Tier skill
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

1. **Qwen Code** - Install from npm
   ```bash
   npm install -g @anthropic/qwen-code
   ```

2. **Python 3.10+** - Download from python.org

3. **Node.js 18+** - Download from nodejs.org

4. **Obsidian** - Download from obsidian.md

### Installation

1. **Install Python dependencies**:
   ```bash
   cd scripts
   pip install -r requirements-silver.txt
   ```

2. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

3. **Install MCP servers**:
   ```bash
   cd mcp-servers/linkedin-mcp && npm install
   cd ../email-mcp && npm install
   ```

4. **Set up environment**:
   ```bash
   cd scripts
   copy .env.example .env
   # Edit .env with your credentials
   ```

5. **Open vault in Obsidian**:
   - Open Obsidian
   - Select `AI_Employee_Vault` folder

---

## 📡 Watchers

### 1. File System Watcher

Monitors drop folder for new files.

```bash
cd scripts
python filesystem_watcher.py ../AI_Employee_Vault
```

**Test:** Drop a file in `AI_Employee_Vault/Inbox/Drop/`

### 2. Gmail Watcher

Monitors Gmail for new unread messages.

**Setup:**
1. Enable Gmail API: https://developers.google.com/gmail/api/quickstart/python
2. Download `credentials.json` to `scripts/` folder
3. First run requires OAuth authorization

```bash
cd scripts
python gmail_watcher.py ../AI_Employee_Vault
```

### 3. WhatsApp Watcher

Monitors WhatsApp Web for messages.

**Setup:**
1. First run requires QR code scan
2. Session saved automatically

```bash
cd scripts
python whatsapp_watcher.py ../AI_Employee_Vault
```

---

## 📮 MCP Servers

### Email MCP Server

Send emails via SMTP with human approval.

**Setup:**
1. Create `.env` in `mcp-servers/email-mcp/`
2. Configure SMTP credentials

```bash
cd mcp-servers/email-mcp
node email_mcp.js
```

**Usage with Qwen:**
```bash
qwen "Create an email draft to client@example.com about the project update"
```

### LinkedIn MCP Server

Post to LinkedIn with human approval.

**Setup:**
1. Create LinkedIn app
2. Get access token
3. Configure `.env`

```bash
cd mcp-servers/linkedin-mcp
node linkedin_mcp.js
```

**Usage with Qwen:**
```bash
qwen "Create a LinkedIn post about our new product launch"
```

---

## 🔄 Human-in-the-Loop Workflow

Silver Tier implements **approval-based actions** for sensitive operations:

### Workflow

1. **AI creates** approval file in `/Pending_Approval/`
2. **Human reviews** the file
3. **Human moves** to `/Approved/` to approve
4. **Approval handler** executes the action
5. **File moved** to `/Done/`
6. **Action logged** in `/Logs/`

### Approval Types

| Action | Auto-Approve | Require Approval |
|--------|--------------|------------------|
| Email to known contacts | ❌ | ✅ Always (Silver Tier) |
| LinkedIn posts | ❌ | ✅ Always |
| Payments | ❌ | ✅ Always |
| File operations | ✅ Read | ❌ Delete |

---

## ⏰ Scheduled Tasks

The scheduler runs automated tasks:

```bash
cd scripts
python scheduler.py ../AI_Employee_Vault
```

### Schedule

| Task | Time | Output |
|------|------|--------|
| Daily Briefing | 8:00 AM | `/Briefings/YYYY-MM-DD_Daily_Briefing.md` |
| CEO Weekly Briefing | Monday 7:00 AM | `/Briefings/YYYY-MM-DD_CEO_Weekly_Briefing.md` |
| Subscription Audit | Sunday 10:00 PM | `/Accounting/YYYY-MM-DD_Subscription_Audit.md` |
| Accounting Sync | 6:00 PM daily | `/Accounting/YYYY-MM-DD_Transactions.md` |

---

## 🤖 Usage Examples

### Process All Pending Files

```bash
cd AI_Employee_Vault
qwen -y "Process all files in /Needs_Action according to Company_Handbook.md"
```

### Create a Plan

```bash
qwen -y "Create a plan in /Plans/ for responding to the urgent client email"
```

### Check Status

```bash
qwen "What's pending in /Needs_Action? Summarize by priority."
```

### Generate Briefing

```bash
qwen "Generate a weekly CEO briefing based on completed tasks"
```

### Approve and Send Email

1. AI creates: `/Pending_Approval/EMAIL_approval_request.md`
2. You review the file
3. Move to `/Approved/` to send
4. Approval handler executes

---

## 🔧 Configuration

### Environment Variables

Create `scripts/.env`:

```env
# Gmail
GMAIL_CREDENTIALS_PATH=./credentials.json

# Email MCP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# LinkedIn
LINKEDIN_ACCESS_TOKEN=your-token
LINKEDIN_PERSON_URN=your-urn

# Vault
VAULT_PATH=./AI_Employee_Vault
```

See `.env.example` for full template.

---

## 🛠️ Troubleshooting

### Gmail Watcher Not Working

1. Check `credentials.json` exists in `scripts/`
2. Delete `token.json` and re-authorize
3. Check Gmail API is enabled

### WhatsApp Not Connecting

1. Delete session folder
2. Re-run watcher
3. Scan QR code promptly

### MCP Server Errors

1. Check `.env` file exists
2. Verify credentials
3. Test connection: `node email_mcp.js` then use `test_connection` tool

### Scheduler Not Running

1. Check Python path
2. Verify APScheduler installed
3. Check logs for errors

---

## 📊 Monitoring

### View Logs

```bash
type Logs\2026-03-31.md
```

### Check Dashboard

Open `Dashboard.md` in Obsidian

### Review Briefings

```bash
type Briefings\*.md
```

---

## 🎯 Next Steps (Gold Tier)

To upgrade to Gold Tier:

1. **Full cross-domain integration** (Personal + Business)
2. **Odoo accounting integration** via MCP
3. **Facebook/Instagram integration**
4. **Twitter (X) integration**
5. **Multiple MCP servers** for different actions
6. **Weekly Business Audit** with CEO Briefing
7. **Error recovery** and graceful degradation
8. **Ralph Wiggum loop** for autonomous completion

---

## 📄 License

Personal AI Employee Hackathon 2026

## 🤝 Contributing

Join the Wednesday Research Meeting:
- **When:** Wednesdays at 10:00 PM
- **Zoom:** [Link in main doc](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)

---

*Silver Tier Complete - Personal AI Employee Hackathon 2026*
