"""
Approval Workflow Handler

Implements Human-in-the-Loop (HITL) approval workflow for Silver Tier.
Monitors /Approved/ folder and executes approved actions.

Usage:
    python approval_handler.py ../AI_Employee_Vault
"""

import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ApprovalHandler:
    """
    Handles approval workflow for sensitive actions.
    
    Monitors /Approved/ folder and executes:
    - Email sending
    - LinkedIn posting
    - Payments (future)
    - Other sensitive actions
    """
    
    def __init__(self, vault_path: str, check_interval: int = 10):
        """
        Initialize the approval handler.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 10)
        """
        self.vault_path = Path(vault_path).resolve()
        self.check_interval = check_interval
        self.logger = logging.getLogger('ApprovalHandler')
        
        # Folders
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        self.pending = self.vault_path / 'Pending_Approval'
        
        # Ensure folders exist
        for folder in [self.approved, self.rejected, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f'ApprovalHandler initialized')
        self.logger.info(f'Vault: {self.vault_path}')
    
    def check_approved_folder(self) -> list:
        """Check for approved files ready to execute."""
        approved_files = []
        
        if self.approved.exists():
            for file_path in self.approved.iterdir():
                if file_path.suffix == '.md':
                    approved_files.append(file_path)
        
        return approved_files
    
    def process_approved_file(self, file_path: Path) -> bool:
        """
        Process an approved file.
        
        Args:
            file_path: Path to the approved file
            
        Returns:
            True if successful
        """
        self.logger.info(f'Processing approved file: {file_path.name}')
        
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Parse frontmatter to get type
            file_type = self._extract_type(content)
            
            # Execute based on type
            if file_type == 'email_approval_request':
                success = self._send_approved_email(file_path, content)
            elif file_type == 'linkedin_post_draft':
                success = self._post_linkedin(file_path, content)
            elif file_type == 'payment_approval':
                success = self._process_payment(file_path, content)
            else:
                self.logger.warning(f'Unknown file type: {file_type}')
                success = False
            
            if success:
                # Move to Done
                dest = self.done / file_path.name
                shutil.move(str(file_path), str(dest))
                self.logger.info(f'Moved to Done: {file_path.name}')
                
                # Log success
                self._log_action('approval_executed', file_path.name, 'success', {'type': file_type})
            else:
                # Log failure
                self._log_action('approval_failed', file_path.name, 'failed', {'type': file_type})
            
            return success
            
        except Exception as e:
            self.logger.error(f'Error processing approved file: {e}', exc_info=True)
            self._log_action('approval_error', file_path.name, 'error', {'error': str(e)})
            return False
    
    def _extract_type(self, content: str) -> str:
        """Extract type from YAML frontmatter."""
        import re
        match = re.search(r'type:\s*(\w+)', content)
        return match.group(1) if match else 'unknown'
    
    def _send_approved_email(self, file_path: Path, content: str) -> bool:
        """Send an approved email."""
        # Extract email details from content
        import re
        
        to_match = re.search(r'\*\*To:\*\*\s*(.+)', content)
        subject_match = re.search(r'\*\*Subject:\*\*\s*(.+)', content)
        body_match = re.search(r'## Content\s*\n```?\n?(.+?)\n?```?', content, re.DOTALL)
        
        if not all([to_match, subject_match, body_match]):
            self.logger.error('Missing email fields')
            return False
        
        to = to_match.group(1).strip()
        subject = subject_match.group(1).strip()
        body = body_match.group(1).strip()
        
        self.logger.info(f'Would send email to: {to}, subject: {subject}')
        
        # For Silver Tier, we log the action but don't actually send
        # In production, integrate with email MCP server here
        
        return True
    
    def _post_linkedin(self, file_path: Path, content: str) -> bool:
        """Post approved LinkedIn content."""
        import re
        
        content_match = re.search(r'## Content\s*\n(.+?)\n##', content, re.DOTALL)
        
        if not content_match:
            self.logger.error('Missing LinkedIn content')
            return False
        
        post_content = content_match.group(1).strip()
        
        self.logger.info(f'Would post to LinkedIn: {post_content[:50]}...')
        
        # For Silver Tier, we log the action but don't actually post
        # In production, integrate with LinkedIn MCP server here
        
        return True
    
    def _process_payment(self, file_path: Path, content: str) -> bool:
        """Process approved payment."""
        import re
        
        amount_match = re.search(r'\*\*Amount:\*\*\s*\$?([\d.]+)', content)
        recipient_match = re.search(r'\*\*Recipient:\*\*\s*(.+)', content)
        
        if not all([amount_match, recipient_match]):
            self.logger.error('Missing payment fields')
            return False
        
        amount = amount_match.group(1)
        recipient = recipient_match.group(1).strip()
        
        self.logger.info(f'Would process payment: ${amount} to {recipient}')
        
        # For Silver Tier, we log the action but don't actually pay
        # In production, integrate with payment API here
        
        return True
    
    def _log_action(self, action_type: str, target: str, status: str, details: Dict = None):
        """Log an action to the logs folder."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            log_file = self.logs / f'{today}.md'
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action_type': action_type,
                'actor': 'approval_handler',
                'target': target,
                'status': status,
                'details': details or {}
            }
            
            content = f'# Logs for {today}\n\n'
            if log_file.exists():
                content = log_file.read_text(encoding='utf-8') + '\n\n'
            
            content += json.dumps(log_entry, indent=2)
            log_file.write_text(content, encoding='utf-8')
            
        except Exception as e:
            self.logger.error(f'Error logging action: {e}')
    
    def run(self):
        """Main run loop."""
        self.logger.info('Starting ApprovalHandler')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                try:
                    approved_files = self.check_approved_folder()
                    
                    if approved_files:
                        self.logger.info(f'Found {len(approved_files)} approved file(s)')
                        
                        for file_path in approved_files:
                            self.process_approved_file(file_path)
                    
                except Exception as e:
                    self.logger.error(f'Error in main loop: {e}', exc_info=True)
                
                import time
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('ApprovalHandler stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python approval_handler.py <vault_path>")
        print("\nExample:")
        print("  python approval_handler.py ../AI_Employee_Vault")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    handler = ApprovalHandler(str(vault_path))
    handler.run()


if __name__ == '__main__':
    main()
