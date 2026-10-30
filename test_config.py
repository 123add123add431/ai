# test_config.py
from unittest.mock import patch
from pydantic import SecretStr
import pytest
from config import Settings

# 1. 测试配置的默认值
def test_default_settings():
    settings = Settings()
    assert isinstance(settings.api_key, SecretStr)
    assert settings.api_key.get_secret_value() == "sk-default-key"
    assert settings.temperature == 0.7

# 2. 测试温度参数的范围校验（0-1之间）
def test_temperature_validation():
    # 正常范围内的值应该成功
    assert Settings(temperature=0.0).temperature == 0.0
    assert Settings(temperature=1.0).temperature == 1.0

    # 超出范围应该抛出异常
    with pytest.raises(ValueError):
        Settings(temperature=-0.1)
    with pytest.raises(ValueError):
        Settings(temperature=1.1)

# 3. 测试从 .env 文件加载配置（模拟读取过程）
@patch.dict('os.environ', {'API_KEY': 'sk-mocked-key', 'TEMPERATURE': '0.8'})
def test_env_variable_override():
    # 强制重新加载配置以读取 mock 的环境变量
    from config import get_settings
    get_settings.cache_clear() 
    settings = get_settings()
    
    assert settings.api_key.get_secret_value() == "sk-mocked-key"
    assert settings.temperature == 0.8