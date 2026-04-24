from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NVIDIA_API_KEY: str
    NVIDIA_API_URL: str = "https://integrate.api.nvidia.com/v1/chat/completions"
    OPENAI_API_BASE: str = "https://integrate.api.nvidia.com/v1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
