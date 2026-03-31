---
name: ai-employee-vault-ops
version: 0.2.0
description: AI Employee Vault Operations - Manage your Personal AI Employee's Obsidian vault (Silver Tier)
author: AI Employee Hackathon 2026
---

# AI Employee Vault Operations Skill

This skill enables Qwen Code to manage and operate a Personal AI Employee's Obsidian vault, including processing action files, managing workflows, and maintaining the dashboard.

**Silver Tier Features:**
- Gmail integration
- WhatsApp Web monitoring
- LinkedIn posting (with approval)
- Email sending (with approval)
- Scheduled daily/weekly briefings
- Human-in-the-loop approval workflow

## Capabilities

- **Read/Write Vault Files**: Access all vault folders and markdown files
- **Process Action Files**: Handle files in `/Needs_Action` folder
- **Create Plans**: Generate step-by-step plans for complex tasks
- **Manage Approvals**: Create and process approval request files
- **Update Dashboard**: Keep the main dashboard current with activity
- **Log Actions**: Maintain audit logs of all operations
- **Move Files**: Transfer files between workflow folders

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md           # Main status dashboard
├── Company_Handbook.md    # Rules and guidelines
├── Business_Goals.md      # Business objectives
├── Inbox/                 # Raw incoming items
│   └── Drop/              # File drop folder (for filesystem_watcher)
├── Needs_Action/          # Items requiring processing
├── Plans/                 # Multi-step task plans
├── Pending_Approval/      # Awaiting human approval
├── Approved/              # Approved for action
├── Rejected/              # Rejected items
├── Done/                  # Completed tasks
├── Logs/                  # Action logs (YYYY-MM-DD.md)
├── Briefings/             # CEO briefings
├── Accounting/            # Financial records
└── Invoices/              # Generated invoices
```

## Usage Examples

### Process All Pending Action Files

```bash
qwen "Check the /Needs_Action folder and process all pending action files according to the Company Handbook"
```

### Create a Plan for a Complex Task

```bash
qwen "Create a plan in /Plans/ for processing the invoice request from Client A"
```

### Request Human Approval

```bash
qwen "Create an approval request file in /Pending_Approval/ for a payment of $150 to Vendor XYZ"
```

### Update Dashboard

```bash
qwen "Update Dashboard.md with today's completed activities and current stats"
```

### Generate Daily Log

```bash
qwen "Create a log entry in /Logs/YYYY-MM-DD.md for the email sent to client@example.com"
```

## Rules of Engagement

Always follow these rules from the Company Handbook:

1. **Approval Thresholds**:
   - Payments over $100 require approval
   - New payees require approval
   - Emails to new contacts require approval

2. **Priority Handling**:
   - Process items marked `priority: urgent` or `priority: high` first
   - Keywords: "urgent", "asap", "invoice", "payment", "help"

3. **Documentation**:
   - Log every action in `/Logs/`
   - Update Dashboard.md after completing tasks
   - Create plans for multi-step tasks

4. **File Movement**:
   - Move completed files to `/Done/`
   - Never delete files without explicit permission
   - Keep the vault organized

## Action File Format

All action files use YAML frontmatter:

```markdown
---
type: file_drop | email | whatsapp | task
source: filesystem | gmail | whatsapp | manual
received: 2026-03-31T10:30:00
priority: low | normal | high | urgent
status: pending | processing | completed
---

# Content

## Suggested Actions
- [ ] Action item 1
- [ ] Action item 2
```

## Approval Request Format

```markdown
---
type: approval_request
action: payment | email | file_operation
amount: 150.00  # For payments
recipient: Vendor XYZ
created: 2026-03-31T10:30:00
status: pending
---

# Approval Request

## Details
- Action: Payment
- Amount: $150.00
- Recipient: Vendor XYZ
- Reason: Invoice #123

## To Approve
Move this file to `/Approved/`

## To Reject
Move this file to `/Rejected/`
```

## Integration with Watchers

This skill works with the watcher scripts:

1. **Filesystem Watcher** (`filesystem_watcher.py`): Monitors drop folder
2. **Gmail Watcher** (future): Monitors Gmail
3. **WhatsApp Watcher** (future): Monitors WhatsApp

Watchers create action files → Claude processes them → Files move to `/Done/`

## Commands

### Check Vault Status
```bash
qwen "Check the AI Employee vault status and report pending items"
```

### Process Specific File
```bash
qwen "Process the action file FILE_invoice_20260331.md in /Needs_Action/"
```

### Generate Briefing
```bash
qwen "Generate a weekly CEO briefing in /Briefings/ with revenue and activity summary"
```

### Audit Logs
```bash
qwen "Review the logs in /Logs/ for this week and summarize all actions taken"
```

## Error Handling

If you encounter errors:

1. **File not found**: Check if the file was moved or deleted
2. **Permission denied**: Create an approval request instead of acting
3. **Ambiguous instructions**: Ask for clarification
4. **System error**: Log the error and alert the user

## Best Practices

1. Always read the Company Handbook before processing
2. Check for existing plans before creating new ones
3. Batch similar actions when possible
4. Keep the dashboard updated in real-time
5. Use clear, descriptive filenames
6. Include timestamps in all logs
7. Never bypass the approval workflow

## Troubleshooting

**Q: Action file not being processed**
A: Check if it has proper YAML frontmatter and .md extension

**Q: Dashboard not updating**
A: Ensure Dashboard.md exists and has the correct sections

**Q: Approval files not being acted upon**
A: Remind the user to move files to /Approved/ or /Rejected/

---

*This skill is part of the Personal AI Employee Hackathon 2026 - Bronze Tier*
