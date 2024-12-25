
import os
import yaml

class Settings:
    def __init__(self, config_dict=None):
        config_dict = config_dict or {}
        self.DEBUG = config_dict.get("DEBUG", True)
        self.DATABASE_URL = config_dict.get("DATABASE_URL", "sqlite:///ignite.db")
        self.SECRET_KEY = config_dict.get("SECRET_KEY", "ignite-secret-key")
        self.JWT_SECRET = config_dict.get("JWT_SECRET", "ignite-jwt-secret")
        self.PLUGINS_FOLDER = config_dict.get("plugins_folder", "plugins")

def load_settings_from_file(config_path: str = "ignite.yaml") -> Settings:
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}. Using default settings.")
        return Settings()

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Settings(data)

settings = Settings()
