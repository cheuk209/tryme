from pydantic_settings import BaseSettings
import logging
from dotenv import load_dotenv
import os
from logging.handlers import RotatingFileHandler

load_dotenv()

class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    USE_AZURE_KEY_VAULT: bool = False
    AZURE_KEY_VAULT_URL: str = ""
    AZURE_KEY_VAULT_SECRET_NAME: str = "ALPHA-VANTAGE-API-KEY"
    class Config:
        env_file = ".env"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.USE_AZURE_KEY_VAULT:
            self._load_from_azure_key_vault()

    def _load_from_azure_key_vault(self):
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=self.AZURE_KEY_VAULT_URL, credential=credential)
        self.ALPHA_VANTAGE_API_KEY = client.get_secret(self.AZURE_KEY_VAULT_SECRET_NAME).value

# Logging files locally
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(logs_dir, 'app.log')
file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)  # 10MB per file, keep 5 old files
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)
settings = Settings()
