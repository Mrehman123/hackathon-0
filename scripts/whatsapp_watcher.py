"""
WhatsApp Watcher

Monitors WhatsApp Web for new messages and creates action files in the vault.
Silver Tier component of the AI Employee system.

Note: This uses WhatsApp Web automation. Be aware of WhatsApp's terms of service.
For production use, consider the official WhatsApp Business API.

Usage:
    python whatsapp_watcher.py ../AI_Employee_Vault
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from base_watcher import BaseWatcher


class WhatsAppWatcher(BaseWatcher):
    """
    Watches WhatsApp Web for new messages.
    
    Creates action files in Needs_Action folder for:
    - Messages containing priority keywords
    - Messages from important contacts
    - Unread messages in business chats
    """
    
    def __init__(self, vault_path: str, session_path: str = None,
                 check_interval: int = 60):
        """
        Initialize the WhatsApp watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            session_path: Path to store browser session (default: vault/Inbox/.whatsapp_session)
            check_interval: Seconds between checks (default: 60)
        """
        super().__init__(vault_path, check_interval)
        
        # Set up session path
        if session_path:
            self.session_path = Path(session_path)
        else:
            self.session_path = self.inbox / '.whatsapp_session'
        
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Priority keywords
        self.priority_keywords = ['urgent', 'asap', 'invoice', 'payment', 
                                   'help', 'emergency', 'deadline', 'important']
        
        self.logger.info(f'WhatsApp Watcher initialized')
        self.logger.info(f'Session path: {self.session_path}')
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new messages in WhatsApp Web.
        
        Returns:
            List of message dictionaries
        """
        messages = []
        
        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                browser = p.chromium.launch_persistent_context(
                    self.session_path,
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                
                # Go to WhatsApp Web
                page.goto('https://web.whatsapp.com', timeout=60000)
                
                try:
                    # Wait for chat list to load
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                    
                    # Find unread chats
                    unread_chats = page.query_selector_all('[aria-label*="unread"]')
                    
                    for chat in unread_chats:
                        try:
                            # Get chat name
                            name_element = chat.query_selector('[dir="auto"]')
                            chat_name = name_element.inner_text() if name_element else 'Unknown'
                            
                            # Get message preview
                            message_element = chat.query_selector('[dir="auto"]:last-child')
                            message_text = message_element.inner_text() if message_element else ''
                            
                            # Check for priority keywords
                            text_lower = message_text.lower()
                            priority = 'high' if any(
                                kw in text_lower for kw in self.priority_keywords
                            ) else 'normal'
                            
                            # Only process high priority or keyword matches
                            if priority == 'high' or any(
                                kw in text_lower for kw in self.priority_keywords
                            ):
                                messages.append({
                                    'chat_name': chat_name,
                                    'message': message_text,
                                    'priority': priority,
                                    'timestamp': datetime.now().isoformat()
                                })
                            
                        except Exception as e:
                            self.logger.debug(f'Error processing chat: {e}')
                            continue
                    
                    browser.close()
                    
                except PlaywrightTimeout:
                    self.logger.warning('WhatsApp Web loading timeout - may need QR scan')
                    browser.close()
                    
        except Exception as e:
            self.logger.error(f'Error checking WhatsApp: {e}')
        
        return messages
    
    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: Dictionary containing message information
            
        Returns:
            Path to the created file, or None if failed
        """
        try:
            # Create YAML frontmatter
            header = self.create_standard_header(
                item_type='whatsapp',
                source='whatsapp_web',
                priority=item.get('priority', 'normal')
            )
            
            # Create content
            content = f"""{header}

# WhatsApp Message

## Message Details
- **From:** {item['chat_name']}
- **Received:** {item['timestamp']}
- **Priority:** {item['priority']}

## Message Content
{item['message']}

## Suggested Actions
- [ ] Read full message
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing

## Notes
Add your response or notes here:

"""
            
            # Generate filename
            safe_name = "".join(c if c.isalnum() else '_' for c in item['chat_name'][:20])
            filename = self.generate_filename('WHATSAPP', safe_name)
            filepath = self.needs_action / filename
            
            # Write file
            filepath.write_text(content, encoding='utf-8')
            
            self.logger.info(f'Processed WhatsApp from: {item["chat_name"]}')
            return filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            return None
    
    def run(self):
        """Main run loop for the WhatsApp watcher."""
        self.logger.info('Starting WhatsApp Watcher')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info('Note: First run requires QR code scan in browser')
        
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
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('WhatsApp Watcher stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise


def main():
    """Main entry point for the WhatsApp watcher."""
    if len(sys.argv) < 2:
        print("Usage: python whatsapp_watcher.py <vault_path> [session_path]")
        print("\nExample:")
        print("  python whatsapp_watcher.py ../AI_Employee_Vault")
        print("  python whatsapp_watcher.py ../AI_Employee_Vault ./whatsapp_session")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    session_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    watcher = WhatsAppWatcher(str(vault_path), str(session_path) if session_path else None)
    watcher.run()


if __name__ == '__main__':
    main()
