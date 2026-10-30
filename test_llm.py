# test_llm.py
import pytest
from unittest.mock import patch, MagicMock, mock_open
from chatbot import ChatBot
from httpx import Response

# 模拟一个假的 API 响应生成器（模拟流式输出）
def mock_stream_response():
    """生成模拟的流式文本数据"""
    yield "我是"
    yield "AI"
    yield "助手。"

# 1. 测试大模型参数传递及 Mock API 返回
@patch("chatbot.httpx.Client")
def test_chatbot_parameters_and_mock(MockClientClass):
    # 初始化机器人
    bot = ChatBot()
    
    # 准备 Mock 对象，模拟 httpx.Client 的 stream 方法和 iter_text
    mock_client_instance = MockClientClass.return_value
    mock_client_instance.__enter__.return_value = mock_client_instance
    mock_client_instance.__exit__.return_value = False
    
    # 模拟 stream 上下文管理器
    mock_stream_instance = MagicMock()
    mock_stream_instance.__enter__.return_value = mock_stream_instance
    mock_stream_instance.__exit__.return_value = False
    mock_stream_instance.status_code = 200
    mock_stream_instance.iter_text.return_value = mock_stream_response()
    
    mock_client_instance.stream.return_value = mock_stream_instance
    
    # 执行聊天
    user_message = "你好"
    result = bot.chat(user_message)
    
    # 验证是否向 API 发送了正确的参数
    MockClientClass.assert_called_once()
    called_with = mock_client_instance.stream.call_args
    
    # 断言：参数中是否包含我们设定的 temperature 和 stream=True
    payload = called_with.kwargs['json']
    assert payload["temperature"] == 0.7  # 验证配置中的默认温度是否被传入
    assert payload["stream"] is True      # 验证是否开启了流式输出
    
    # 验证 Mock 返回的结果是否被正确拼接到历史记录中
    assert "我是" in bot.history[-1]["content"]
    assert "AI" in bot.history[-1]["content"]
    assert "助手。" in bot.history[-1]["content"]