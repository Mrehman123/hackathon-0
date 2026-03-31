"""
File System Watcher

Monitors a drop folder for new files and creates action files in the vault.
This is the Bronze Tier watcher - simple, reliable, and doesn't require API setup.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder
"""

import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handler for file system events in the drop folder."""
    
    def __init__(self, watcher: 'FileSystemWatcher'):
        self.watcher = watcher
        self.logger = self.watcher.logger
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        source = Path(event.src_path)
        self.logger.info(f'New file detected: {source.name}')
        
        # Create action file for this new file
        item = {
            'path': source,
            'name': source.name,
            'size': source.stat().st_size,
            'created': datetime.fromtimestamp(source.stat().st_ctime)
        }
        
        self.watcher.process_new_file(item)


class FileSystemWatcher(BaseWatcher):
    """
    Watches a drop folder for new files.
    
    When a file is added, it:
    1. Copies the file to the vault
    2. Creates a metadata .md file in Needs_Action
    3. Claude can then process the file based on Company_Handbook rules
    """
    
    def __init__(self, vault_path: str, drop_folder: str = None, 
                 check_interval: int = 5):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            drop_folder: Path to the drop folder (default: vault/Inbox/Drop)
            check_interval: Seconds between checks (default: 5 for responsive file drops)
        """
        super().__init__(vault_path, check_interval)
        
        # Set up drop folder
        if drop_folder:
            self.drop_folder = Path(drop_folder)
        else:
            self.drop_folder = self.inbox / 'Drop'
        
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        self.files_folder = self.vault_path / 'Files'
        self.files_folder.mkdir(parents=True, exist_ok=True)
        
        # Priority keywords
        self.priority_keywords = ['urgent', 'asap', 'invoice', 'payment', 
                                   'help', 'emergency', 'deadline']
        
        self.logger.info(f'Drop folder: {self.drop_folder}')
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new files in the drop folder.
        
        Returns:
            List of file info dictionaries
        """
        new_files = []
        
        for file_path in self.drop_folder.iterdir():
            if file_path.is_file() and not file_path.suffix == '.md':
                file_id = self._get_file_hash(file_path)
                
                if not self.is_processed(file_id):
                    new_files.append({
                        'path': file_path,
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                        'id': file_id
                    })
        
        return new_files
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Generate a unique hash for a file."""
        stat = file_path.stat()
        content = f"{file_path.name}{stat.st_size}{stat.st_mtime}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def process_new_file(self, item: Dict[str, Any]):
        """Process a newly detected file."""
        try:
            file_path = item['path']
            file_id = item.get('id', self._get_file_hash(file_path))
            
            # Copy file to vault/Files
            dest_path = self.files_folder / file_path.name
            shutil.copy2(file_path, dest_path)
            self.logger.info(f'Copied file to vault: {dest_path.name}')
            
            # Create action file
            action_file = self.create_action_file({
                'name': file_path.name,
                'size': file_path.stat().st_size,
                'path': dest_path,
                'id': file_id
            })
            
            # Remove from drop folder after processing
            file_path.unlink()
            self.logger.info(f'Removed from drop folder: {file_path.name}')
            
            # Mark as processed
            self.mark_as_processed(file_id)
            
            return action_file
            
        except Exception as e:
            self.logger.error(f'Error processing file {item["name"]}: {e}')
            return None
    
    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: Dictionary containing file information
            
        Returns:
            Path to the created file, or None if failed
        """
        try:
            # Determine priority based on filename
            priority = 'normal'
            name_lower = item['name'].lower()
            if any(keyword in name_lower for keyword in self.priority_keywords):
                priority = 'high'
            
            # Create YAML frontmatter
            header = self.create_standard_header(
                item_type='file_drop',
                source='filesystem',
                priority=priority
            )
            
            # Create content
            content = f"""{header}

# File Drop for Processing

## File Information
- **Original Name:** {item['name']}
- **Size:** {self._format_size(item['size'])}
- **Location:** {item['path']}
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions
- [ ] Review file contents
- [ ] Categorize file type
- [ ] Take appropriate action based on Company Handbook
- [ ] Move to /Done when complete

## Notes
Add your processing notes here:

"""
            
            # Generate filename
            filename = self.generate_filename('FILE', item['name'][:20])
            filepath = self.needs_action / filename
            
            # Write file
            filepath.write_text(content, encoding='utf-8')
            
            return filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def run_with_observer(self):
        """
        Run the watcher using watchdog observer (more efficient than polling).
        This is the recommended way to run the file system watcher.
        """
        self.logger.info(f'Starting FileSystemWatcher with observer')
        self.logger.info(f'Drop folder: {self.drop_folder}')
        
        event_handler = DropFolderHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info('FileSystemWatcher stopped by user')
        
        observer.join()


def main():
    """Main entry point for the filesystem watcher."""
    if len(sys.argv) < 2:
        print("Usage: python filesystem_watcher.py <vault_path> [drop_folder]")
        print("\nExample:")
        print("  python filesystem_watcher.py ./AI_Employee_Vault")
        print("  python filesystem_watcher.py ./AI_Employee_Vault ./drop_folder")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    drop_folder = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    watcher = FileSystemWatcher(str(vault_path), str(drop_folder) if drop_folder else None)
    
    # Use observer-based watching (more efficient)
    watcher.run_with_observer()


if __name__ == '__main__':
    main()
