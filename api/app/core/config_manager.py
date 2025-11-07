from pathlib import Path
import shutil
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize ConfigManager with optional config path.
        If no path is provided, uses default locations.
        """
        self.config_path = Path(config_path) if config_path else self._find_config()
        self.config: Dict[str, Any] = {}
        self._ensure_config_exists()
        self.load_config()

    def _find_config(self) -> Path:
        """
        Search for config file in standard locations:
        1. Current directory
        2. User's home directory
        3. /etc/slow-query-doctor
        """
        search_paths = [
            Path.cwd() / ".slow-query-doctor.yml",
            Path.cwd() / "config.yml",
            Path.home() / ".slow-query-doctor.yml",
            Path("/etc/slow-query-doctor/config.yml"),
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        # If no config found, use the current directory
        return Path.cwd() / ".slow-query-doctor.yml"

    def _ensure_config_exists(self) -> None:
        """
        Create default config file if none exists.
        """
        if not self.config_path.exists():
            logger.info(f"No config file found at {self.config_path}. Creating default config...")
            self._create_default_config()

    def _create_default_config(self) -> None:
        """
        Copy default config template to config location.
        """
        template_path = Path(__file__).parent.parent / "templates" / "config.default.yml"
        
        # Create parent directories if they don't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy default config
        shutil.copy(template_path, self.config_path)
        logger.info(f"Created default config at {self.config_path}")

    def load_config(self) -> None:
        """
        Load configuration from file.
        """
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading config from {self.config_path}: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key with optional default.
        Supports nested keys with dot notation (e.g., 'api.port').
        """
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key.
        Supports nested keys with dot notation.
        """
        keys = key.split('.')
        current = self.config
        
        # Navigate to the correct nesting level
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value

    def save(self) -> None:
        """
        Save current configuration to file.
        """
        try:
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(self.config, f, default_flow_style=False)
            logger.info(f"Saved configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving config to {self.config_path}: {e}")
            raise

    def reload(self) -> None:
        """
        Reload configuration from file.
        """
        self.load_config()

# Global config instance
config_manager = ConfigManager()