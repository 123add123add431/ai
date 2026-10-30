# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic import SecretStr

class Settings(BaseSettings):
    # API_KEY 使用 SecretStr 类型，更安全
    api_key: SecretStr = SecretStr("sk-default-key")
    # 对话温度，范围在 0-1 之间
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

    class Config:
        env_file = ".env"  # 可以从 .env 文件读取配置
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    """使用 lru_cache 缓存配置，避免重复读取"""
    return Settings()

# 创建一个全局可用的配置实例
settings = get_settings()