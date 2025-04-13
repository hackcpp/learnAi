

使用 **Print日志** 进行LangChain应用调试的详细步骤指南，包含代码示例和调试技巧：

---

### **1. 基础调试模板**
#### 代码结构示例
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 定义链
chain = (
    ChatPromptTemplate.from_template("将'{text}'翻译成{lang}") 
    | ChatOpenAI() 
    | StrOutputParser()
)

# 执行链
result = chain.invoke({"text": "Hello", "lang": "法语"})
print("最终结果:", result)
```

---

### **2. 分阶段调试步骤**
#### 步骤1：检查提示模板输出
```python
# 在提示模板后添加打印
prompt = ChatPromptTemplate.from_template("将'{text}'翻译成{lang}")
debug_prompt = prompt | (lambda x: print("提示内容:\n", x.to_messages()) or x)

chain = debug_prompt | ChatOpenAI() | StrOutputParser()
```
**输出示例**：
```
提示内容:
 [HumanMessage(content="将'Hello'翻译成法语")]
```

#### 步骤2：捕获模型原始响应
```python
# 在模型调用后添加打印
model = ChatOpenAI()
debug_model = model | (lambda x: print("模型原始响应:\n", x) or x)

chain = prompt | debug_model | StrOutputParser()
```
**输出示例**：
```
模型原始响应:
 AIMessage(content='Bonjour')
```

#### 步骤3：验证输出解析
```python
# 在解析器前添加打印
parser = StrOutputParser()
debug_parser = (lambda x: print("解析前内容:\n", x) or x) | parser

chain = prompt | ChatOpenAI() | debug_parser
```
**输出示例**：
```
解析前内容:
 AIMessage(content='Bonjour')
最终结果: Bonjour
```

---

### **3. 流式处理调试**
#### 流式输出捕获
```python
# 流式处理调试链
stream_chain = (
    ChatPromptTemplate.from_template("用50字描述{object}")
    | ChatOpenAI(streaming=True)
    | StrOutputParser()
)

print("流式输出开始 ▶")
for chunk in stream_chain.stream({"object": "区块链"}):
    print("收到分块:", chunk)  # 显示每个数据块
print("◀ 流式输出结束")
```
**输出示例**：
```
流式输出开始 ▶
收到分块: 区块
收到分块: 链是一种
收到分块: 分布式账本技术...
◀ 流式输出结束
```

---

### **4. 异步调用调试**
#### 异步日志记录
```python
import asyncio

async def debug_async():
    # 定义带日志的异步链
    chain = (
        ChatPromptTemplate.from_template("将'{text}'翻译成{lang}")
        | ChatOpenAI()
        | {"response": StrOutputParser()}
    )
  
    print("异步调用开始")
    result = await chain.ainvoke({"text": "Goodbye", "lang": "德语"})
    print("异步结果:", result)
    return result

asyncio.run(debug_async())
```
**输出示例**：
```
异步调用开始
异步结果: {'response': 'Auf Wiedersehen'}
```

---

### **5. 复杂链调试技巧**
#### 技巧1：标记执行阶段
```python
def log_stage(stage_name):
    def logger(data):
        print(f"\n=== {stage_name} ===")
        print("输入:", data)
        return data
    return logger

chain = (
    log_stage("初始化输入") 
    | prompt 
    | log_stage("提示处理后") 
    | model 
    | log_stage("模型响应后")
    | parser
)
```

#### 技巧2：数据快照保存
```python
import json

def save_snapshot(data):
    with open("debug_snapshot.json", "w") as f:
        json.dump({"data": data}, f, ensure_ascii=False)
    return data

chain = prompt | model | save_snapshot | parser
```

---

### **6. 调试场景实战**
#### 场景：处理异常输入
```python
def safe_processing(data):
    try:
        if not isinstance(data["text"], str):
            raise ValueError("text字段必须为字符串")
        return data
    except Exception as e:
        print(f"输入校验失败: {str(e)}")
        raise

debug_chain = (
    (lambda x: safe_processing(x))
    | prompt
    | model
    | parser
)

# 测试错误输入
debug_chain.invoke({"text": 123, "lang": "中文"})
```
**输出**：
```
输入校验失败: text字段必须为字符串
ValidationError...
```

---

### **7. 调试日志最佳实践**
1. **日志分级控制**
```python
DEBUG_LEVEL = 3  # 1:基础 2:详细 3:全量

def debug_log(content, level=1):
    if level <= DEBUG_LEVEL:
        print(f"[DEBUG{level}] {content}")

# 使用示例
debug_log("收到用户输入", 1)
```

2. **时间戳标记**
```python
from datetime import datetime

def timestamp_log(msg):
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{now}] {msg}")

timestamp_log("链开始执行")
```

3. **敏感信息过滤**
```python
def secure_print(data):
    filtered = {k: "***" if "key" in k else v 
               for k,v in data.items()}
    print("安全输出:", filtered)
    return data

chain = prompt | model | secure_print | parser
```

---

### **Print调试 vs LangSmith**
| 维度             | Print日志                          | LangSmith                         |
|------------------|------------------------------------|-----------------------------------|
| 设置复杂度       | 简单（无需配置）                  | 需要API密钥和网络连接            |
| 历史记录追溯     | ❌ 只能查看当次运行               | ✅ 永久保存所有运行记录           |
| 执行可视化       | ❌ 纯文本输出                     | ✅ 图形化流程跟踪                |
| 性能影响         | 可能降低执行速度                  | 几乎无影响                       |
| 多线程/异步支持  | 需要处理输出顺序                  | ✅ 自动处理并发场景              |
| 适用阶段         | 开发初期/简单问题                 | 生产环境/复杂问题分析            |

---

通过合理插入print语句，开发者可以快速定位以下典型问题：
1. **提示模板错误**：检查实际生成的提示内容
2. **类型不匹配**：查看各环节的数据结构
3. **模型响应异常**：捕获原始API返回数据
4. **解析失败**：验证解析前的中间数据
5. **异步执行顺序**：跟踪任务调度时序

建议在开发初期使用print调试快速验证核心逻辑，在复杂场景切换至LangSmith进行深度分析。