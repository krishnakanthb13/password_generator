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
    
    def log(self, result: Any) -> None:
        """
        Log a generator result.
        
        Args:
            result: GeneratorResult object to log
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "password": result.password,
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
        limit: int = 10,
        search: Optional[str] = None,
        generator_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get password generation history.
        
        Args:
            limit: Maximum entries to return
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
                    
                    # Apply filters
                    if search and search.lower() not in json.dumps(entry).lower():
                        continue
                    if generator_type and entry.get('generator_type') != generator_type:
                        continue
                    
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue
        
        # Return most recent first
        entries.reverse()
        return entries[:limit]
    
    def clear_history(self) -> None:
        """Clear all password history."""
        if self.log_file.exists():
            self.log_file.unlink()
    
    def export_history(self, output_path: str, format: str = "json") -> None:
        """
        Export history to a file.
        
        Args:
            output_path: Path to output file
            format: Export format ('json' or 'csv')
        """
        entries = self.get_history(limit=10000)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2)
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if entries:
                    writer = csv.DictWriter(f, fieldnames=['timestamp', 'generator_type', 'password', 'entropy_bits'])
                    writer.writeheader()
                    for entry in entries:
                        writer.writerow({
                            'timestamp': entry['timestamp'],
                            'generator_type': entry['generator_type'],
                            'password': entry['password'],
                            'entropy_bits': entry['entropy_bits']
                        })
