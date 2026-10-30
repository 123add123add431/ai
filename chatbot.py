# chatbot.py
import httpx
from config import settings

# 假设的 API 端点，请根据你的实际作业文档替换
API_URL = "https://api.example.com/chat"

class ChatBot:
    def __init__(self):
        # 存储对话历史
        self.history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def chat(self, user_message: str):
        # 1. 将用户消息添加到历史记录中
        self.history.append({"role": "user", "content": user_message})

        # 2. 准备发送给 API 的数据
        payload = {
            "messages": self.history,
            "model": "gpt-3.5-turbo",  # 示例模型
            "temperature": settings.temperature,
            "stream": True  # 开启流式输出
        }
        
        # 3. 调用 API（这里用 httpx 进行演示）
        # 注意：这里需要传入 api_key
        headers = {
            "Authorization": f"Bearer {settings.api_key.get_secret_value()}",
            "Content-Type": "application/json"
        }

        print(f"\n你: {user_message}")
        print("助手: ", end="")

        response_text = ""
        with httpx.Client(headers=headers) as client:
            with client.stream("POST", API_URL, json=payload) as response:
                for chunk in response.iter_text():
                    if chunk:
                        # 简单的流式处理，实际可能需要解析 SSE 格式
                        print(chunk, end="", flush=True)
                        response_text += chunk

        # 4. 将助手的回复添加到历史记录中，保持连续对话
        self.history.append({"role": "assistant", "content": response_text.strip()})
        print("\n") # 打印一个空行，使输出更整洁
        return response_text.strip()

if __name__ == "__main__":
    bot = ChatBot()
    print("=== 欢迎来到聊天机器人！输入 'quit' 或 'exit' 退出 ===")
    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ('quit', 'exit'):
            print("助手: 再见！")
            break
        if not user_input:
            continue
        bot.chat(user_input)