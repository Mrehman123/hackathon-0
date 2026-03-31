---
name: ai-employee-silver-tier
version: 0.2.0
description: Complete Silver Tier skills for AI Employee
author: AI Employee Hackathon 2026
---

# AI Employee - Silver Tier Skills

This document describes all skills available in the Silver Tier implementation.

## 🎯 Silver Tier Deliverables

✅ Two or more Watcher scripts (Gmail + WhatsApp + File System)  
✅ Automatically Post on LinkedIn (with approval)  
✅ Qwen reasoning loop that creates Plan.md files  
✅ One working MCP server for external action (Email)  
✅ Human-in-the-loop approval workflow  
✅ Basic scheduling via Task Scheduler  
✅ All AI functionality as Agent Skills  

---

## 📡 Watcher Skills

### 1. Gmail Watcher (`gmail_watcher.py`)

**Purpose:** Monitor Gmail for new unread messages

**Setup:**
1. Enable Gmail API: https://developers.google.com/gmail/api/quickstart/python
2. Download `credentials.json` and place in `scripts/` folder
3. First run requires OAuth authorization

**Usage:**
```bash
cd scripts
python gmail_watcher.py ../AI_Employee_Vault
```

**Creates action files for:**
- Unread messages from important contacts
- Messages with urgent keywords (invoice, payment, urgent, asap)
- Messages with attachments

**Action File Format:**
```markdown
---
type: email
source: gmail
received: 2026-03-31T10:30:00
priority: high
status: pending
---

# Email from client@example.com

## Message Details
- **From:** client@example.com
- **Subject:** Invoice Payment Urgent
- **Date:** Mon, 31 Mar 2026 10:30:00 +0000

## Preview
Please process the invoice payment as soon as possible...

## Suggested Actions
- [ ] Read full email
- [ ] Reply to sender
- [ ] Process payment
```

---

### 2. WhatsApp Watcher (`whatsapp_watcher.py`)

**Purpose:** Monitor WhatsApp Web for new messages

**Setup:**
- First run requires QR code scan to authenticate WhatsApp Web
- Session is stored in `vault/Inbox/.whatsapp_session`

**Usage:**
```bash
cd scripts
python whatsapp_watcher.py ../AI_Employee_Vault
```

**Creates action files for:**
- Messages containing priority keywords
- Unread messages from business contacts

**Action File Format:**
```markdown
---
type: whatsapp
source: whatsapp_web
received: 2026-03-31T10:30:00
priority: high
status: pending
---

# WhatsApp Message

## Message Details
- **From:** John Doe
- **Received:** 2026-03-31T10:30:00
- **Priority:** high

## Message Content
Hey, can you send me the invoice for January? It's urgent.

## Suggested Actions
- [ ] Read full message
- [ ] Reply to sender
- [ ] Generate invoice
```

---

### 3. File System Watcher (`filesystem_watcher.py`)

**Purpose:** Monitor drop folder for new files

**Usage:**
```bash
cd scripts
python filesystem_watcher.py ../AI_Employee_Vault
```

**Creates action files for:**
- Any file dropped in `vault/Inbox/Drop/`
- Priority based on filename keywords

---

## 📮 MCP Server Skills

### 1. Email MCP Server (`mcp-servers/email-mcp/`)

**Purpose:** Send emails via SMTP with human approval

**Setup:**
1. Create `.env` file in `mcp-servers/email-mcp/`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

2. For Gmail, use App Password:
   - Go to Google Account → Security
   - Enable 2FA
   - Create App Password

**Usage:**
```bash
cd mcp-servers/email-mcp
node email_mcp.js
```

**Tools:**
- `send_email` - Send email (creates approval file for Silver Tier)
- `create_email_draft` - Create draft for review
- `test_connection` - Test SMTP connection

**HITL Pattern:**
Emails create approval files in `/Pending_Approval/` that must be moved to `/Approved/` before sending.

---

### 2. LinkedIn MCP Server (`mcp-servers/linkedin-mcp/`)

**Purpose:** Post updates to LinkedIn with human approval

**Setup:**
1. Create LinkedIn app: https://www.linkedin.com/developers/apps
2. Get access token
3. Create `.env` file:
```env
LINKEDIN_ACCESS_TOKEN=your-access-token
LINKEDIN_PERSON_URN=your-person-urn
```

**Usage:**
```bash
cd mcp-servers/linkedin-mcp
node linkedin_mcp.js
```

**Tools:**
- `post_to_linkedin` - Create LinkedIn post (approval required)
- `create_linkedin_draft` - Create draft for review

**Example Post:**
```bash
qwen "Create a LinkedIn post about our new product launch"
```

---

## 🔄 Approval Workflow Skills

### Approval Handler (`approval_handler.py`)

**Purpose:** Execute approved actions from `/Approved/` folder

**Usage:**
```bash
cd scripts
python approval_handler.py ../AI_Employee_Vault
```

**Workflow:**
1. AI creates approval file in `/Pending_Approval/`
2. Human reviews and moves to `/Approved/`
3. Approval handler executes the action
4. File moved to `/Done/`
5. Action logged in `/Logs/`

**Approval Types:**
- Email sending
- LinkedIn posting
- Payment processing (future)

---

## ⏰ Scheduler Skills

### Scheduler (`scheduler.py`)

**Purpose:** Run scheduled tasks for daily/weekly operations

**Usage:**
```bash
cd scripts
python scheduler.py ../AI_Employee_Vault
```

**Scheduled Tasks:**

| Task | Schedule | Description |
|------|----------|-------------|
| Daily Briefing | 8:00 AM daily | Generate daily task summary |
| CEO Weekly Briefing | Monday 7:00 AM | Weekly business review |
| Subscription Audit | Sunday 10:00 PM | Review recurring expenses |
| Accounting Sync | 6:00 PM daily | Sync transactions |

**Generated Files:**
- `/Briefings/YYYY-MM-DD_Daily_Briefing.md`
- `/Briefings/YYYY-MM-DD_CEO_Weekly_Briefing.md`
- `/Accounting/YYYY-MM-DD_Subscription_Audit.md`

---

## 🤖 Qwen Integration

### Processing Action Files

```bash
cd AI_Employee_Vault
qwen -y "Process all files in /Needs_Action according to Company_Handbook.md"
```

### Creating Plans

```bash
qwen -y "Create a plan in /Plans/ for responding to the urgent email from client"
```

### Generating Briefings

```bash
qwen -y "Generate a weekly CEO briefing based on completed tasks and business goals"
```

---

## 📋 Complete Workflow Example

### Scenario: Client asks for invoice via WhatsApp

1. **WhatsApp Watcher** detects message with "invoice" keyword
2. Creates action file in `/Needs_Action/`
3. **Orchestrator** triggers Qwen to process
4. **Qwen** reads Company_Handbook.md for rules
5. **Qwen** creates Plan.md with steps
6. **Qwen** generates invoice (if data available)
7. **Qwen** creates email draft in `/Pending_Approval/`
8. **Human** reviews and moves to `/Approved/`
9. **Approval Handler** sends email via MCP
10. File moved to `/Done/`
11. Action logged in `/Logs/`

---

## 🔧 Configuration Files

### `.env` Template

```env
# Gmail API
GMAIL_CREDENTIALS_PATH=./credentials.json

# WhatsApp
WHATSAPP_SESSION_PATH=./whatsapp_session

# Email MCP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# LinkedIn MCP
LINKEDIN_ACCESS_TOKEN=your-access-token
LINKEDIN_PERSON_URN=your-person-urn

# Vault
VAULT_PATH=./AI_Employee_Vault
```

---

## 🚀 Quick Start Commands

```bash
# Start all watchers (Terminal 1-3)
cd scripts
python filesystem_watcher.py ../AI_Employee_Vault
python gmail_watcher.py ../AI_Employee_Vault
python whatsapp_watcher.py ../AI_Employee_Vault

# Start approval handler (Terminal 4)
python approval_handler.py ../AI_Employee_Vault

# Start scheduler (Terminal 5)
python scheduler.py ../AI_Employee_Vault

# Process files with Qwen
cd AI_Employee_Vault
qwen -y "Process all pending action files"
```

---

## 📊 Monitoring

### Check Status
```bash
qwen "What's pending in /Needs_Action?"
```

### View Logs
```bash
type Logs\2026-03-31.md
```

### Check Dashboard
```bash
qwen "Update Dashboard.md with today's activity"
```

---

*Silver Tier - Personal AI Employee Hackathon 2026*
