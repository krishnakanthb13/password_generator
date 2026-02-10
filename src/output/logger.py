"""
Password Logger - Log generated passwords with history viewer.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class PasswordLogger:
    """Log generated passwords to a JSON Lines file."""
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory for log files (default: ~/.passforge/)
        """
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = Path.home() / ".passforge"
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "pass_history.log"
        
        try:
            from ..security.vault import Vault
            self.vault = Vault(self.log_dir)
        except ImportError:
            self.vault = None
    
    def log(self, result: Any) -> None:
        """
        Log a generator result.
        
        Args:
            result: GeneratorResult object to log
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "password": self.vault.encrypt(result.password),
            "generator_type": result.generator_type,
            "entropy_bits": round(result.entropy_bits, 2),
            "parameters": result.parameters
        }
        
        try:
            # Append to log file (JSON Lines format)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + "\n")
        except (IOError, OSError):
            # Fail silently to avoid interrupting user flow
            pass
    
    def get_history(
        self,
        limit: Optional[int] = 10,
        search: Optional[str] = None,
        generator_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get password generation history.
        
        Args:
            limit: Maximum entries to return (set to None for all)
            search: Search term to filter results
            generator_type: Filter by generator type
            
        Returns:
            List of log entries
        """
        if not self.log_file.exists():
            return []
        
        entries = []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    
                    # Decrypt password for viewing/searching
                    if 'password' in entry:
                        entry['password'] = self.vault.decrypt(entry['password'])
                    
                    # Apply filters
                    if search and search.lower() not in json.dumps(entry).lower():
                        continue
                    if generator_type and entry.get('generator_type') != generator_type:
                        continue
                    
                    entries.append(entry)
                except Exception:
                    continue
        
        # Return most recent first
        entries.reverse()
        
        if limit is None:
            return entries
        return entries[:limit]
    
    def clear_history(self) -> None:
        """Clear all password history."""
        if self.log_file.exists():
            self.log_file.unlink()
    
    def export_history(self, output_path: str, format: str = "json", redact_passwords: bool = True) -> None:
        """
        Export history to a file.
        
        SECURITY WARNING: Exporting without redaction (redact_passwords=False) will 
        save all your passwords in plain text to the destination file. Use with extreme 
        caution as this bypasses the security vault.
        
        Args:
            output_path: Path to output file
            format: Export format ('json' or 'csv')
            redact_passwords: If True (default), passwords are replaced by "<REDACTED>".
        """
        import logging
        log_helper = logging.getLogger(__name__)

        if not redact_passwords:
            log_helper.warning(f"SENSITIVE DATA EXPORT: Exporting history to {output_path} with plaintext passwords.")

        entries = self.get_history(limit=10000)
        
        # Process entries for export (redaction or formatting)
        export_data = []
        for entry in entries:
            # We create a copy to avoid modifying the in-memory history if cached (though it's currently not)
            clean_entry = entry.copy()
            if redact_passwords:
                clean_entry['password'] = "<REDACTED>"
            export_data.append(clean_entry)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if export_data:
                    writer = csv.DictWriter(f, fieldnames=['timestamp', 'generator_type', 'password', 'entropy_bits'])
                    writer.writeheader()
                    for entry in export_data:
                        writer.writerow({
                            'timestamp': entry['timestamp'],
                            'generator_type': entry['generator_type'],
                            'password': entry['password'],
                            'entropy_bits': entry['entropy_bits']
                        })
