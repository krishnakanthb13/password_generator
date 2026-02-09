"""
Configuration file loader for PassForge.
Supports YAML and JSON configuration files.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    """Load and manage PassForge configuration."""
    
    # Default configuration values
    DEFAULTS = {
        "random": {
            "length": 16,
            "uppercase": True,
            "lowercase": True,
            "digits": True,
            "symbols": True,
            "easy_read": False,
            "easy_say": False
        },
        "passphrase": {
            "words": 4,
            "separator": "-",
            "capitalize": False
        },
        "leetspeak": {
            "words": 3,
            "separator": "-"
        },
        "pin": {
            "length": 6
        },
        "pronounceable": {
            "length": 12
        },
        "uuid": {
            "uppercase": False
        },
        "base64": {
            "bytes": 32,
            "url_safe": True
        },
        "jwt": {
            "bits": 256,
            "output_hex": False
        },
        "wifi": {
            "length": 16,
            "simple": False
        },
        "license": {
            "segments": 4,
            "segment_length": 4
        },
        "recovery": {
            "count": 10,
            "use_words": False
        },
        "otp": {
            "digits": 6,
            "period": 30
        },
        "pattern": {
            "grid_size": 3,
            "path_length": 5
        },
        "output": {
            "show_entropy": False,
            "json": False,
            "no_color": False,
            "log": False
        },
        "history": {
            "enabled": True,
            "max_entries": 1000
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the config loader.
        
        Args:
            config_path: Path to config file, or None for default locations
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = self.DEFAULTS.copy()
        self._load_config()
    
    def _find_config_file(self) -> Optional[Path]:
        """Find configuration file in standard locations."""
        search_paths = [
            Path.cwd() / "passforge.yaml",
            Path.cwd() / "passforge.yml",
            Path.cwd() / "passforge.json",
            Path.cwd() / ".passforge.yaml",
            Path.cwd() / ".passforge.json",
            Path.home() / ".passforge" / "config.yaml",
            Path.home() / ".passforge" / "config.yml",
            Path.home() / ".passforge" / "config.json",
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        return None
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path:
            config_file = Path(self.config_path)
        else:
            config_file = self._find_config_file()
        
        if not config_file or not config_file.exists():
            return
        
        try:
            content = config_file.read_text(encoding='utf-8')
            
            if config_file.suffix in ['.yaml', '.yml']:
                try:
                    import yaml
                    loaded = yaml.safe_load(content)
                except ImportError:
                    print("Warning: PyYAML not installed, skipping YAML config")
                    return
            else:
                loaded = json.loads(content)
            
            if loaded:
                self._merge_config(loaded)
                
        except Exception as e:
            print(f"Warning: Failed to load config from {config_file}: {e}")
    
    def _merge_config(self, loaded: Dict[str, Any]) -> None:
        """Merge loaded config with defaults."""
        for key, value in loaded.items():
            if key in self.config and isinstance(self.config[key], dict) and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Config section (e.g., 'random', 'passphrase')
            key: Config key within section
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        section_config = self.config.get(section, {})
        return section_config.get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire configuration section.
        
        Args:
            section: Config section name
            
        Returns:
            Dictionary of section settings
        """
        return self.config.get(section, {})
    
    def save_defaults(self, path: Optional[str] = None) -> None:
        """
        Save default configuration to a file.
        
        Args:
            path: Output path, or None for ~/.passforge/config.json
        """
        if path:
            output_path = Path(path)
        else:
            output_path = Path.home() / ".passforge" / "config.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.DEFAULTS, f, indent=2)
        
        print(f"Default configuration saved to: {output_path}")


# Global config instance
_config: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """Get or create the global config instance."""
    global _config
    if _config is None:
        _config = ConfigLoader()
    return _config


def reload_config(config_path: Optional[str] = None) -> ConfigLoader:
    """Reload configuration from file."""
    global _config
    _config = ConfigLoader(config_path)
    return _config
