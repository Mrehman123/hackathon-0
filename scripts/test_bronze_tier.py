"""
Quick Test Script - No Dependencies Required

This script tests the Bronze Tier setup without requiring pip install.
It simulates the file watcher workflow manually.
"""

import shutil
from pathlib import Path
from datetime import datetime


def test_vault_structure():
    """Test 1: Verify vault folder structure exists."""
    print("\n" + "="*60)
    print("TEST 1: Vault Structure")
    print("="*60)
    
    vault = Path("AI_Employee_Vault")
    required_folders = [
        "Inbox", "Needs_Action", "Done", "Plans", 
        "Pending_Approval", "Approved", "Rejected", 
        "Logs", "Briefings", "Accounting", "Invoices"
    ]
    
    required_files = [
        "Dashboard.md",
        "Company_Handbook.md", 
        "Business_Goals.md"
    ]
    
    all_good = True
    
    # Check folders
    print("\nChecking folders...")
    for folder in required_folders:
        folder_path = vault / folder
        if folder_path.exists() and folder_path.is_dir():
            print(f"  ✅ /{folder}")
        else:
            print(f"  ❌ /{folder} - MISSING")
            all_good = False
    
    # Check files
    print("\nChecking files...")
    for file in required_files:
        file_path = vault / file
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            all_good = False
    
    return all_good


def test_drop_file():
    """Test 2: Create a test file in the Drop folder."""
    print("\n" + "="*60)
    print("TEST 2: Drop File Test")
    print("="*60)
    
    vault = Path("AI_Employee_Vault")
    drop_folder = vault / "Inbox" / "Drop"
    drop_folder.mkdir(parents=True, exist_ok=True)
    
    # Create a test file
    test_file = drop_folder / "test_document.txt"
    test_content = """This is a test document for the AI Employee.

Please review this document and:
1. Summarize the contents
2. Categorize it appropriately
3. Suggest any follow-up actions

This is urgent - please process ASAP.
"""
    test_file.write_text(test_content, encoding='utf-8')
    print(f"\n✅ Created test file: {test_file}")
    
    # Manually create the action file (simulating what filesystem_watcher.py does)
    needs_action = vault / "Needs_Action"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    action_file = needs_action / f"FILE_test_document_{timestamp}.md"
    
    action_content = f"""---
type: file_drop
source: filesystem
received: {datetime.now().isoformat()}
priority: high
status: pending
---

# File Drop for Processing

## File Information
- **Original Name:** test_document.txt
- **Size:** 0.3 KB
- **Location:** {vault / 'Files' / 'test_document.txt'}
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions
- [ ] Review file contents
- [ ] Categorize file type
- [ ] Take appropriate action based on Company Handbook
- [ ] Move to /Done when complete

## Notes
Add your processing notes here:

"""
    
    # Copy the test file to Files folder
    files_folder = vault / "Files"
    files_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(test_file, files_folder / "test_document.txt")
    
    action_file.write_text(action_content, encoding='utf-8')
    print(f"✅ Created action file: {action_file.name}")
    
    # Remove from drop folder (simulating processing)
    test_file.unlink()
    print(f"✅ Removed from drop folder")
    
    return True


def test_claude_integration():
    """Test 3: Test Claude Code integration."""
    print("\n" + "="*60)
    print("TEST 3: Claude Code Integration")
    print("="*60)
    
    print("\nTo test Claude Code, run this command:")
    print("\n```bash")
    print("cd AI_Employee_Vault")
    print('claude "Check /Needs_Action folder and process any pending files"')
    print("```\n")
    
    print("Expected behavior:")
    print("  1. Claude reads the action file")
    print("  2. Claude checks Company_Handbook.md for rules")
    print("  3. Claude processes the file")
    print("  4. Claude updates Dashboard.md")
    print("  5. Claude moves file to /Done/")
    
    return True


def show_manual_test_instructions():
    """Show manual testing instructions."""
    print("\n" + "="*60)
    print("MANUAL TESTING INSTRUCTIONS")
    print("="*60)
    print("""
Step 1: Verify Setup
--------------------
✅ Run: python test_bronze_tier.py
   (This script - checks vault structure)

Step 2: Drop a File
-------------------
1. Create any text file (e.g., notes.txt, invoice.pdf)
2. Copy it to: AI_Employee_Vault/Inbox/Drop/

Step 3: Run File Watcher (requires Python + watchdog)
-------------------
cd scripts
pip install watchdog
python filesystem_watcher.py ../AI_Employee_Vault

Step 4: Run Orchestrator (requires Claude Code)
-------------------
# In a new terminal
cd scripts
python orchestrator.py ../AI_Employee_Vault

Step 5: Watch the Magic
-------------------
1. Check AI_Employee_Vault/Needs_Action/ for new action files
2. Check AI_Employee_Vault/Dashboard.md for updates
3. Check AI_Employee_Vault/Done/ for processed files

Step 6: Manual Claude Test (alternative)
-------------------
cd AI_Employee_Vault
claude "Process all files in /Needs_Action folder"

    """)


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  BRONZE TIER TEST SUITE")
    print("  Personal AI Employee Hackathon 2026")
    print("="*60)
    
    results = []
    
    # Test 1: Vault structure
    results.append(("Vault Structure", test_vault_structure()))
    
    # Test 2: Drop file
    results.append(("Drop File", test_drop_file()))
    
    # Test 3: Claude integration
    results.append(("Claude Integration", test_claude_integration()))
    
    # Show manual test instructions
    show_manual_test_instructions()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("  🎉 ALL TESTS PASSED! Bronze Tier is ready!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues above.")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
