

 **LCEL 代码示例**

---

### **1. 基础链式处理（完整可运行版本）**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 定义提示模板
prompt = ChatPromptTemplate.from_template(
    "用不超过50字总结以下文本：\n\n{text}"
)

# 初始化模型
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.5,
    openai_api_key="sk-your-key"  # 替换实际API Key
)

# 构建LCEL链
chain = prompt | llm | StrOutputParser()

# 执行调用
input_text = """LangChain是一个用于开发语言模型应用的框架，
它提供了模块化组件和链式调用能力，可以快速构建复杂的AI应用。"""
result = chain.invoke({"text": input_text})

print(result)
# 输出：LangChain是用于构建语言模型应用的框架，提供模块化组件和链式调用，便于开发复杂AI应用。
```

---

### **2. 条件分支处理（完整实现）**
```python
from langchain_core.runnables import RunnableBranch

# 定义子链
tech_prompt = ChatPromptTemplate.from_template(
    "作为科技作者，用专业术语解释：{concept}"
)
sports_prompt = ChatPromptTemplate.from_template(
    "作为体育解说员，用生动语言描述：{concept}"
)
general_prompt = ChatPromptTemplate.from_template(
    "用通俗语言解释：{concept}"
)

tech_chain = tech_prompt | llm | StrOutputParser()
sports_chain = sports_prompt | llm | StrOutputParser()
general_chain = general_prompt | llm | StrOutputParser()

# 构建分支逻辑
branch_chain = RunnableBranch(
    (lambda x: x["topic"] == "科技", tech_chain),
    (lambda x: x["topic"] == "体育", sports_chain),
    general_chain
)

# 完整执行链
full_chain = RunnableParallel({  # 并行处理输入
    "concept": lambda x: x["concept"],
    "topic": lambda x: x["topic"]
}) | branch_chain

# 测试不同分支
print(full_chain.invoke({
    "concept": "神经网络", 
    "topic": "科技"
}))
# 输出包含"神经元"、"反向传播"等术语

print(full_chain.invoke({
    "concept": "越位", 
    "topic": "体育"
}))
# 输出包含"足球比赛"、"裁判判罚"等描述
```

---

### **3. 并行处理与结果合并**
```python
from langchain_core.runnables import RunnableParallel

# 定义子链
summary_chain = (
    ChatPromptTemplate.from_template("总结文本：{text}")
    | llm 
    | StrOutputParser()
)

sentiment_chain = (
    ChatPromptTemplate.from_template("分析文本情感倾向：{text}")
    | llm 
    | StrOutputParser()
)

# 并行处理链
parallel_chain = RunnableParallel({
    "summary": summary_chain,
    "sentiment": sentiment_chain
})

# 执行
input_data = {"text": "这款手机拍照效果出色，但电池续航较差"}
result = parallel_chain.invoke(input_data)

print(f"总结：{result['summary']}")
# 输出：总结：该手机拍照功能优秀，但电池续航能力不足
print(f"情感：{result['sentiment']}")
# 输出：情感：正面与负面评价并存
```

---

### **4. 流式输出实现**
```python
# 流式处理链
stream_chain = (
    ChatPromptTemplate.from_template("用100字描述{object}")
    | ChatOpenAI(streaming=True)  # 必须启用流式
    | StrOutputParser()
)

# 逐词输出
for chunk in stream_chain.stream({"object": "量子计算机"}):
    print(chunk, end="", flush=True)
# 输出示例：量子计算机...利用...量子比特...并行计算...
```

---

### **5. 异步调用与批处理**
```python
import asyncio

# 异步链
async_chain = (
    ChatPromptTemplate.from_template("将'{word}'翻译成{lang}")
    | ChatOpenAI()
    | StrOutputParser()
)

# 批量异步处理
async def main():
    inputs = [
        {"word": "hello", "lang": "法语"},
        {"word": "world", "lang": "西班牙语"}
    ]
    return await async_chain.abatch(inputs)

results = asyncio.run(main())
print(results)  # 输出：['Bonjour', 'Mundo']
```

---

### **6. 自定义函数集成**
```python
from langchain_core.runnables import RunnableLambda

# 自定义校验函数
def validate_length(text: str) -> str:
    if len(text) < 20:
        raise ValueError("文本需至少20字符")
    return text

# 链中加入验证
full_chain = (
    ChatPromptTemplate.from_template("生成关于{theme}的短文")
    | llm 
    | StrOutputParser()
    | RunnableLambda(validate_length)
)

try:
    full_chain.invoke({"theme": "AI"})  # 触发异常
except ValueError as e:
    print(f"验证失败：{e}")
```

---

### **7. 调试配置示例**
```python
from langchain_core.runnables import RunnableConfig

# 配置跟踪参数
config = RunnableConfig(
    run_name="production_chain",
    tags=["v2.1", "summarization"],
    metadata={"department": "marketing"}
)

# 带配置执行
chain = (
    ChatPromptTemplate.from_template("总结市场报告：{report}")
    | llm.with_config(config) 
    | StrOutputParser()
)

result = chain.invoke({
    "report": "2023年Q4销售额增长20%..."
}, config=config)
```

---

### **代码运行准备**
1. 安装必要依赖：
```bash
pip install langchain-core langchain-openai python-dotenv
```
2. 创建 `.env` 文件：
```ini
OPENAI_API_KEY=sk-your-key
```
3. 在代码开头加载环境变量：
```python
from dotenv import load_dotenv
load_dotenv()  # 自动读取.env文件
```

所有示例均可直接复制到 `.py` 文件中运行（需替换实际API密钥），建议从简单链开始逐步增加复杂度。遇到类型错误时，使用 `print(chain.input_schema.schema())` 查看输入格式要求。