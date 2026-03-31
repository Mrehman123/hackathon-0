# AI Employee - Quick Test Guide

## ✅ Installation Complete!

- **Python:** 3.13.2 ✅
- **Watchdog:** 6.0.0 ✅
- **Claude Code:** 2.1.72 ✅

## Running the AI Employee

### Step 1: Start the Services

Two processes are now running in the background:
1. **File System Watcher** - Monitors the Drop folder for new files
2. **Orchestrator** - Processes action files with Claude Code

### Step 2: Test the Workflow

#### Option A: Drop a File (Automatic)

1. Create a text file with instructions, e.g., `task.txt`:
   ```
   Please summarize this document and categorize it.
   Also suggest any follow-up actions needed.
   
   Priority: HIGH
   ```

2. Copy it to: `AI_Employee_Vault\Inbox\Drop\`

3. The watcher will:
   - Detect the new file
   - Copy it to `Files/` folder
   - Create an action file in `Needs_Action/`
   - The orchestrator will process it with Claude

4. Check results in:
   - `Dashboard.md` - Updated activity
   - `Done/` - Processed files
   - `Logs/` - Action logs

#### Option B: Manual Claude Test

Open a new terminal and run:

```bash
cd AI_Employee_Vault
claude "Check /Needs_Action folder and process all pending action files according to Company_Handbook.md"
```

### Step 3: Monitor Activity

Check these files to see what happened:

1. **Dashboard.md** - Real-time status
2. **Logs/YYYY-MM-DD.md** - Today's action logs
3. **Done/** - Completed action files

## Current Status

Action files waiting in `Needs_Action/`:
- FILE_test_document_20260331_215521.md
- FILE_test_document_20260331_223027.md

## Stop the Services

To stop the background processes:

```bash
taskkill /F /T /PID 20500
taskkill /F /T /PID 19604
```

## Troubleshooting

### Watcher not detecting files?
- Ensure the file is copied to `AI_Employee_Vault\Inbox\Drop\`
- Check that watchdog is installed: `pip show watchdog`

### Orchestrator not processing?
- Check Claude Code is installed: `claude --version`
- Verify the vault path is correct
- Check logs in `Logs/` folder

### Need to restart?
```bash
# Stop existing processes
taskkill /F /T /PID 20500
taskkill /F /T /PID 19604

# Start fresh (in separate terminals)
cd scripts
python filesystem_watcher.py ../AI_Employee_Vault
python orchestrator.py ../AI_Employee_Vault
```

---

*Bronze Tier - Personal AI Employee Hackathon 2026*
