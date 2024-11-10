from dotenv import load_dotenv
import os
from typing import Dict, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigLoader:
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the configuration by loading environment variables."""
        # Find the .env file - look in parent directories if not found
        env_path = self._find_env_file()
        
        # Load environment variables from .env file
        load_dotenv(env_path)
        
        # Define configuration with defaults
        self._config = {
            # Server Configuration
            "HOST": os.getenv("HOST", "0.0.0.0"),
            "PORT": int(os.getenv("PORT", 8000)),
            "DEBUG": os.getenv("DEBUG", "False").lower() == "true",
            
            # Database Configuration
            "DATABASE_URL": os.getenv("DATABASE_URL", "postgresql://ai_agent_user:secure_password@db:5432/ai_agent_db"),
            "ELASTICSEARCH_URL": os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200"),
            
            # Slack Configuration
            "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
            "SLACK_SIGNING_SECRET": os.getenv("SLACK_SIGNING_SECRET"),
            
            # Ollama Configuration
            "OLLAMA_HOST": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "llama2"),
            
            # Security Configuration
            "SECRET_KEY": os.getenv("SECRET_KEY", "your-secret-key"),
            "CORS_ORIGINS": os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
            
            # GitHub Configuration
            "GITHUB_ACCESS_TOKEN": os.getenv("GITHUB_ACCESS_TOKEN"),
        }
        
        # Validate required configuration
        self._validate_config()
        
        logger.info("Configuration loaded successfully")
    
    def _find_env_file(self) -> Path:
        """Find the .env file by looking in the current and parent directories."""
        current_dir = Path.cwd()
        while current_dir.parent != current_dir:
            env_file = current_dir / ".env"
            if env_file.exists():
                logger.info(f"Found .env file at: {env_file}")
                return env_file
            current_dir = current_dir.parent
        
        # If no .env file is found, use the default location
        logger.warning("No .env file found, using default configuration")
        return Path(".env")
    
    def _validate_config(self):
        """Validate required configuration values."""
        required_keys = [
            "DATABASE_URL",
            "ELASTICSEARCH_URL",
            "SECRET_KEY"
        ]
        
        missing_keys = [key for key in required_keys if not self._config.get(key)]
        if missing_keys:
            logger.warning(f"Missing required configuration keys: {', '.join(missing_keys)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Get a configuration value using dictionary syntax."""
        return self._config[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return key in self._config
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return self._config.copy()

# Create a global instance
config = ConfigLoader()

# Example usage:
# from app.config.config_loader import config
# database_url = config.get("DATABASE_URL")
# slack_token = config["SLACK_BOT_TOKEN"] 