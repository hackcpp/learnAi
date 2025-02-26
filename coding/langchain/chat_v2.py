from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from os import getenv

load_dotenv("../../.env",override=True)  # 加载环境变量

key = getenv("SF_API_KEY") 
url = getenv("SF_API_BASE")
model = getenv("SF_MODEL")

# print(key, url, model)

messages = [
    SystemMessage("你是一个AI助手，请用中文回答问题。")
]

def main():
    chat = ChatDeepSeek(
        model=model,
        api_key=key,
        api_base=url,
    )

    print("欢迎使用AI聊天助手！输入/help查看帮助")
    while True:
        user_input = input("> ")
        
        if user_input == "/bye":
            print("再见！")
            break
        elif user_input == "/help":
            print_help()
        elif user_input == "/reset":
            reset_context()
            print("对话上下文已重置。")
        else:
            response = get_ai_response(chat, user_input)
            print(f"\nAI助手：{response}\n")

def reset_context():
    global messages
    messages = [
        SystemMessage("你是一个AI助手，请用中文回答问题。")
    ]

def print_help():
    help_text = """
可用命令：
/help  显示帮助信息
/bye   退出程序
/reset 清除上下文

其他输入将作为问题发送给AI助手
"""
    print(help_text)

def get_ai_response(chat, prompt):
    try:
        message = HumanMessage(prompt)
        messages.append(message)
        message = chat.invoke(messages)
        messages.append(message)
        return message.content
    except Exception as e:
        return f"请求出错：{str(e)}"

if __name__ == "__main__":
    main()
