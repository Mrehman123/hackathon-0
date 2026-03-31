# AI Employee - Bronze Tier Test Guide (Qwen Version)

## ✅ Installation Complete!

| Component | Status              | Version |
| --------- | ------------------- | ------- |
| Python    | ✅ Installed         | 3.13.2  |
| Watchdog  | ✅ Installed         | 6.0.0   |
| Qwen Code | ⚠️ Install Required | -       |

---

## 🚀 How to Test Bronze Tier with Qwen

### Step 1: Install Qwen Code (If Not Installed)

```bash
npm install -g @anthropic/qwen-code
```

Verify installation:
```bash
qwen --version
```

### Step 2: Test with Qwen

#### Option A: Direct Test (Recommended)

1. **Open Terminal** (cmd or PowerShell)

2. **Navigate to vault**:
   ```bash
   cd C:\Users\LEN\Documents\GitHub\hackathon-0\AI_Employee_Vault
   ```

3. **Run Qwen**:
   ```bash
   qwen
   ```

4. **When prompted to trust the folder, type `1`**

5. **Paste this prompt**:
   ```
   You are the AI Employee. Please:
   
   1. Read Company_Handbook.md to understand your rules
   2. Check /Needs_Action folder for action files
   3. Process each file according to the Handbook
   4. Update Dashboard.md with your activity
   5. Create a log entry in /Logs/2026-03-31.md
   6. Move processed files to /Done/
   
   Report what you find and what actions you take.
   ```

6. **Check results**:
   - Open `Dashboard.md` - Should show new activity
   - Open `Done/` folder - Should contain processed files
   - Open `Logs/2026-03-31.md` - Should have log entries

---

#### Option B: File Drop Test (With Watcher)

**Terminal 1: Start the File Watcher**

```bash
cd C:\Users\LEN\Documents\GitHub\hackathon-0\scripts
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','User')
python filesystem_watcher.py ../AI_Employee_Vault
```

**Now drop a file:**

1. Create a text file (e.g., `task.txt`) with content:
   ```
   Please review this task and create a summary.
   Priority: HIGH - Process ASAP
   ```

2. Copy it to:
   ```
   AI_Employee_Vault\Inbox\Drop\
   ```

3. The watcher will automatically:
   - ✅ Detect the new file
   - ✅ Copy it to `Files/` folder
   - ✅ Create an action file in `Needs_Action/`

**Terminal 2: Process with Qwen**

```bash
cd C:\Users\LEN\Documents\GitHub\hackathon-0\AI_Employee_Vault
qwen "Process the new action file in Needs_Action folder"
```

---

### Step 3: Verify Results

Check these files to see what happened:

1. **Dashboard.md** - Real-time status updates
2. **Logs/2026-03-31.md** - Action logs
3. **Done/** - Completed action files
4. **Needs_Action/** - Should be empty after processing

---

## 📋 Quick Reference Commands

### Check what's waiting
```bash
cd AI_Employee_Vault
qwen "What files are in /Needs_Action? Summarize them."
```

### Process all pending files
```bash
qwen "Process all files in /Needs_Action according to Company_Handbook.md"
```

### Check system status
```bash
qwen "Check Dashboard.md and report the current state of the AI Employee system"
```

### Review logs
```bash
qwen "Read /Logs/2026-03-31.md and summarize all actions taken today"
```

---

## 🛠️ Troubleshooting

### Qwen not found
```bash
npm install -g @anthropic/qwen-code
```

### Python not found
Close and reopen terminal, or run:
```bash
refreshenv
```

### Watcher not starting
Make sure you're in the scripts directory and PATH is set:
```bash
cd scripts
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','User')
python filesystem_watcher.py ../AI_Employee_Vault
```

### Qwen asks to trust folder
This is a one-time security check. Type `1` to trust.

---

## 📊 Current Test Files

Action files ready for processing:
- `AI_Employee_Vault/Needs_Action/FILE_test_document_20260331_215521.md`
- `AI_Employee_Vault/Needs_Action/FILE_test_document_20260331_223027.md`

Test document:
- `AI_Employee_Vault/Files/test_document.txt`

---

## ✅ Test Checklist

- [ ] Qwen Code installed (`qwen --version`)
- [ ] Python installed (`python --version`)
- [ ] Watchdog installed (`pip show watchdog`)
- [ ] Vault structure exists (all folders and files)
- [ ] Qwen can access vault (type `1` to trust)
- [ ] Action files processed successfully
- [ ] Dashboard.md updated
- [ ] Logs created
- [ ] Files moved to Done/

---

*Bronze Tier - Personal AI Employee Hackathon 2026 (Qwen Code Version)*
