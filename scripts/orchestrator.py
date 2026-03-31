"""
Orchestrator

Master process that:
1. Watches the Needs_Action folder for new items
2. Triggers Claude Code to process items
3. Updates the Dashboard.md with activity
4. Manages the overall AI Employee workflow

Usage:
    python orchestrator.py /path/to/vault
"""

import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Coordinates between watchers, Claude Code, and the vault.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 10):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 10)
        """
        self.vault_path = Path(vault_path).resolve()
        self.check_interval = check_interval
        self.logger = logging.getLogger('Orchestrator')
        
        # Vault folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure folders exist
        for folder in [self.needs_action, self.done, self.plans, 
                       self.pending_approval, self.approved, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # State tracking
        self.processing_files: set = set()
        self.processed_count = 0
        self.start_time = datetime.now()
        
        self.logger.info(f'Orchestrator initialized')
        self.logger.info(f'Vault path: {self.vault_path}')
    
    def check_needs_action(self) -> List[Path]:
        """
        Check for new .md files in Needs_Action folder.
        
        Returns:
            List of file paths to process
        """
        files = []
        
        if self.needs_action.exists():
            for file_path in self.needs_action.iterdir():
                if file_path.suffix == '.md' and file_path not in self.processing_files:
                    files.append(file_path)
        
        return files
    
    def process_file(self, file_path: Path) -> bool:
        """
        Process a single action file using Claude Code.
        
        Args:
            file_path: Path to the action file
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f'Processing: {file_path.name}')
        self.processing_files.add(file_path)
        
        try:
            # Read the file to understand its type
            content = file_path.read_text(encoding='utf-8')
            
            # Create a prompt for Claude
            prompt = self._create_prompt(file_path, content)
            
            # Run Claude Code
            result = self._run_claude(prompt)
            
            if result:
                self.processed_count += 1
                self.logger.info(f'Successfully processed: {file_path.name}')
                return True
            else:
                self.logger.warning(f'Claude returned no result for: {file_path.name}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error processing {file_path.name}: {e}', exc_info=True)
            return False
        
        finally:
            self.processing_files.discard(file_path)
    
    def _create_prompt(self, file_path: Path, content: str) -> str:
        """
        Create a prompt for Claude Code based on the action file.
        
        Args:
            file_path: Path to the action file
            content: Content of the action file
            
        Returns:
            Prompt string for Claude
        """
        return f"""You are the AI Employee. Process this action file according to the Company Handbook rules.

Action File: {file_path.name}

Content:
{content}

Instructions:
1. Read the Company_Handbook.md for rules of engagement
2. Determine what type of action this is (file_drop, email, whatsapp, etc.)
3. Check if any approval is required based on the Handbook
4. If approval needed, create a file in /Pending_Approval/
5. If no approval needed, take the action and document it
6. Update Dashboard.md with the activity
7. Move this file to /Done/ when complete
8. Log the action in /Logs/YYYY-MM-DD.md

Remember:
- Always be professional
- Flag payments over $100 for approval
- Log every action
- Ask for clarification if instructions are ambiguous

Respond with your actions taken, then move the file to /Done/."""
    
    def _run_qwen(self, prompt: str) -> bool:
        """
        Run Qwen Code with the given prompt.
        
        Note: Qwen Code requires interactive terminal for first-run trust.
        For automated processing, use manual Qwen invocation.
        
        Args:
            prompt: Prompt to send to Qwen
            
        Returns:
            True if Qwen executed successfully
        """
        try:
            # Create a state file for manual Qwen processing
            # This is the Bronze Tier approach - Qwen processes files when user invokes it
            self.logger.info('Bronze Tier: Manual Qwen processing required')
            self.logger.info('Run: cd AI_Employee_Vault && qwen "Process /Needs_Action files"')
            return True  # File is ready for processing, Qwen will handle it manually
                
        except Exception as e:
            self.logger.error(f'Error preparing for Qwen: {e}')
            return False
    
    def update_dashboard(self, action: str, details: str = ''):
        """
        Update the Dashboard.md with recent activity.
        
        Args:
            action: Description of the action
            details: Additional details
        """
        try:
            if not self.dashboard.exists():
                self.logger.warning('Dashboard.md not found')
                return
            
            content = self.dashboard.read_text(encoding='utf-8')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            # Add to recent activity section
            activity_line = f"- [{timestamp}] {action}"
            if details:
                activity_line += f" - {details}"
            
            # Find the Recent Activity section and add the line
            lines = content.split('\n')
            new_lines = []
            in_recent_activity = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                if '## ✅ Recent Activity' in line:
                    in_recent_activity = True
                    # Add the new activity after the header
                    if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith('-'):
                        new_lines.append(activity_line)
                        in_recent_activity = False
                    elif i + 1 < len(lines) and (lines[i + 1].startswith('##') or lines[i + 1].startswith('---')):
                        # Next section starts immediately, insert before it
                        new_lines.append(activity_line)
                        in_recent_activity = False
            
            # If we didn't find a good place, add after the header
            if in_recent_activity:
                # Find the header and add after it
                for i, line in enumerate(new_lines):
                    if '## ✅ Recent Activity' in line:
                        # Check if next line is empty or another section
                        if i + 1 >= len(new_lines) or new_lines[i + 1].startswith('##'):
                            new_lines.insert(i + 1, activity_line)
                        break
            
            self.dashboard.write_text('\n'.join(new_lines), encoding='utf-8')
            self.logger.debug('Dashboard updated')
            
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')
    
    def log_action(self, action_type: str, target: str, status: str, 
                   details: Dict[str, Any] = None):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action (file_process, approval_request, etc.)
            target: Target of the action (file name, contact, etc.)
            status: Status (success, pending, failed)
            details: Additional details dictionary
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            log_file = self.logs / f'{today}.md'
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action_type': action_type,
                'actor': 'orchestrator',
                'target': target,
                'status': status,
                'details': details or {}
            }
            
            if log_file.exists():
                content = log_file.read_text(encoding='utf-8')
                # Append to existing log
                content += f'\n\n{json.dumps(log_entry, indent=2)}'
            else:
                content = f'# Logs for {today}\n\n{json.dumps(log_entry, indent=2)}'
            
            log_file.write_text(content, encoding='utf-8')
            self.logger.debug(f'Action logged: {action_type} - {target}')
            
        except Exception as e:
            self.logger.error(f'Error logging action: {e}')
    
    def check_approved_folder(self):
        """
        Check the Approved folder for files ready to execute.
        """
        if not self.approved.exists():
            return
        
        for file_path in self.approved.iterdir():
            if file_path.suffix == '.md':
                self.logger.info(f'Executing approved action: {file_path.name}')
                # Execute the approved action
                self.process_file(file_path)
    
    def run(self):
        """
        Main run loop for the orchestrator.
        """
        self.logger.info('Starting Orchestrator')
        self.logger.info(f'Checking every {self.check_interval} seconds')
        
        try:
            while True:
                try:
                    # Check for new action files
                    files = self.check_needs_action()
                    
                    if files:
                        self.logger.info(f'Found {len(files)} action file(s)')
                        
                        for file_path in files:
                            success = self.process_file(file_path)
                            
                            if success:
                                self.update_dashboard(
                                    action=f'Processed {file_path.name}',
                                    details='Completed successfully'
                                )
                                self.log_action(
                                    action_type='file_process',
                                    target=file_path.name,
                                    status='success'
                                )
                            else:
                                self.log_action(
                                    action_type='file_process',
                                    target=file_path.name,
                                    status='failed'
                                )
                    
                    # Check approved folder
                    self.check_approved_folder()
                    
                    # Update dashboard with stats periodically
                    if self.processed_count % 5 == 0 and self.processed_count > 0:
                        self.update_dashboard(
                            action=f'System Stats',
                            details=f'Processed {self.processed_count} items since {self.start_time.strftime("%H:%M")}'
                        )
                    
                except Exception as e:
                    self.logger.error(f'Error in main loop: {e}', exc_info=True)
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info(f'Orchestrator stopped by user')
            self.logger.info(f'Total items processed: {self.processed_count}')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


class VaultEventHandler(FileSystemEventHandler):
    """Event handler for vault folder changes."""
    
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.logger = logging.getLogger('VaultEventHandler')
    
    def on_created(self, event):
        """Handle new files in Needs_Action."""
        if not event.is_directory and 'Needs_Action' in event.src_path:
            self.logger.info(f'New action file detected: {Path(event.src_path).name}')
            # Could trigger immediate processing here if needed


def main():
    """Main entry point for the orchestrator."""
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <vault_path>")
        print("\nExample:")
        print("  python orchestrator.py ./AI_Employee_Vault")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(str(vault_path))
    orchestrator.run()


if __name__ == '__main__':
    main()
