"""
Gmail Watcher

Monitors Gmail for new unread messages and creates action files in the vault.
Silver Tier component of the AI Employee system.

Setup:
1. Enable Gmail API: https://developers.google.com/gmail/api/quickstart/python
2. Download credentials.json and place in scripts/ folder
3. First run will require OAuth authorization

Usage:
    python gmail_watcher.py ../AI_Employee_Vault
"""

import sys
import os
import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from email import message_from_bytes

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from base_watcher import BaseWatcher

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher(BaseWatcher):
    """
    Watches Gmail for new unread messages.
    
    Creates action files in Needs_Action folder for:
    - Unread messages from important contacts
    - Messages with urgent keywords
    - Messages with attachments
    """
    
    def __init__(self, vault_path: str, credentials_path: str = None, 
                 check_interval: int = 120):
        """
        Initialize the Gmail watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            credentials_path: Path to Gmail credentials JSON (default: credentials.json)
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        
        # Set up credentials path
        if credentials_path:
            self.credentials_path = Path(credentials_path)
        else:
            self.credentials_path = Path(__file__).parent / 'credentials.json'
        
        self.token_path = Path(__file__).parent / 'token.json'
        self.processed_ids: set = set()
        
        # Priority keywords
        self.priority_keywords = ['urgent', 'asap', 'invoice', 'payment', 
                                   'help', 'emergency', 'deadline', 'important']
        
        # Gmail service
        self.service = None
        self._authenticate()
        
        self.logger.info(f'Gmail Watcher initialized')
    
    def _authenticate(self):
        """Authenticate with Gmail API."""
        try:
            creds = None
            
            # Load token if exists
            if self.token_path.exists():
                creds = Credentials.from_authorized_user_file(
                    self.token_path, SCOPES
                )
            
            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not self.credentials_path.exists():
                        self.logger.error(
                            'credentials.json not found! '
                            'Download from https://developers.google.com/gmail/api/quickstart/python'
                        )
                        raise FileNotFoundError('credentials.json not found')
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0, open_browser=False)
                    self.logger.info('Please open the URL in your browser to authorize Gmail access')
                
                # Save token
                self.token_path.write_text(creds.to_json())
            
            # Build service
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info('Gmail authentication successful')
            
        except Exception as e:
            self.logger.error(f'Authentication failed: {e}')
            raise
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new unread messages in Gmail.
        
        Returns:
            List of message dictionaries
        """
        if not self.service:
            self.logger.error('Gmail service not initialized')
            return []
        
        try:
            # Get unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            new_messages = []
            
            for msg in messages:
                msg_id = msg['id']
                if not self.is_processed(msg_id):
                    new_messages.append({'id': msg_id})
            
            return new_messages
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            return []
        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []
    
    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: Dictionary containing message ID
            
        Returns:
            Path to the created file, or None if failed
        """
        try:
            # Get full message
            message = self.service.users().messages().get(
                userId='me',
                id=item['id'],
                format='full'
            ).execute()
            
            # Extract headers
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            from_email = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', '')
            
            # Determine priority
            priority = 'normal'
            subject_lower = subject.lower()
            if any(keyword in subject_lower for keyword in self.priority_keywords):
                priority = 'high'
            
            # Get snippet (preview text)
            snippet = message.get('snippet', '')
            
            # Check for attachments
            has_attachments = any(
                part['filename'] 
                for part in message['payload'].get('parts', [])
            )
            
            # Create YAML frontmatter
            header = self.create_standard_header(
                item_type='email',
                source='gmail',
                priority=priority
            )
            
            # Create content
            content = f"""{header}

# Email from {from_email}

## Message Details
- **From:** {from_email}
- **Subject:** {subject}
- **Date:** {date}
- **Message ID:** {item['id']}
- **Has Attachments:** {has_attachments}

## Preview
{snippet}

## Suggested Actions
- [ ] Read full email
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
- [ ] Flag for follow-up

## Notes
Add your response or notes here:

"""
            
            # Generate filename
            safe_subject = "".join(c if c.isalnum() else '_' for c in subject[:30])
            filename = self.generate_filename('EMAIL', safe_subject)
            filepath = self.needs_action / filename
            
            # Write file
            filepath.write_text(content, encoding='utf-8')
            
            # Mark as processed
            self.mark_as_processed(item['id'])
            
            # Mark as read in Gmail
            self.service.users().messages().modify(
                userId='me',
                id=item['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            self.logger.info(f'Processed email: {subject}')
            return filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            return None
    
    def run(self):
        """Main run loop for the Gmail watcher."""
        self.logger.info('Starting Gmail Watcher')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    self.logger.debug(f'Found {len(items)} new messages')
                    
                    for item in items:
                        filepath = self.create_action_file(item)
                        if filepath:
                            self.logger.info(f'Created action file: {filepath.name}')
                            
                except Exception as e:
                    self.logger.error(f'Error processing messages: {e}', exc_info=True)
                
                # Re-authenticate every hour
                if datetime.now().minute == 0:
                    self._authenticate()
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Gmail Watcher stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


def main():
    """Main entry point for the Gmail watcher."""
    if len(sys.argv) < 2:
        print("Usage: python gmail_watcher.py <vault_path> [credentials_path]")
        print("\nExample:")
        print("  python gmail_watcher.py ../AI_Employee_Vault")
        print("  python gmail_watcher.py ../AI_Employee_Vault ./gmail_credentials.json")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    credentials_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    watcher = GmailWatcher(str(vault_path), str(credentials_path) if credentials_path else None)
    watcher.run()


if __name__ == '__main__':
    main()
