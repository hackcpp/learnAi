

**LangChain逐日详细执行计划**，

---

### **阶段一：基础准备（3天）**
#### **Day 1：环境搭建与API配置**
1. **安装Python 3.10**
   ```bash
   # Mac/Linux
   brew install python@3.10
   # Windows：官网下载安装包
   ```
2. **创建虚拟环境**
   ```bash
   python -m venv langchain-env
   source langchain-env/bin/activate  # Mac/Linux
   .\langchain-env\Scripts\activate   # Windows
   ```
3. **安装核心库**
   ```bash
   pip install langchain openai python-dotenv
   ```
4. **配置OpenAI API密钥**
   ```python
   # .env文件
   OPENAI_API_KEY="sk-your-key"
   ```
   ```python
   # 测试代码 test_api.py
   from dotenv import load_dotenv
   from langchain.llms import OpenAI
   load_dotenv()
   print(OpenAI()("你好！"))  # 应返回AI回复
   ```

#### **Day 2：核心概念实践**
1. **PromptTemplate动态生成**
   ```python
   from langchain.prompts import PromptTemplate
   prompt = PromptTemplate.from_template("用{style}风格解释{concept}")
   print(prompt.format(style="幽默", concept="神经网络"))  # 输出模板
   ```
2. **结构化输出解析**
   ```python
   from langchain.output_parsers import PydanticOutputParser
   from pydantic import BaseModel
   class Joke(BaseModel):
       setup: str
       punchline: str
   parser = PydanticOutputParser(pydantic_object=Joke)
   prompt = PromptTemplate(
       template="讲一个关于{theme}的笑话\n{format_instructions}",
       input_variables=["theme"],
       partial_variables={"format_instructions": parser.get_format_instructions()}
   )
   ```

#### **Day 3：完整流程Demo**
```python
# demo.py
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.7)
prompt = PromptTemplate.from_template("{input}，用步骤列表说明")
chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run("如何泡一杯好茶"))
```
**输出验证**：确保返回分步骤的泡茶指南

---

### **阶段二：核心模块深度掌握（2周）**
#### **模块1：Model I/O（3天）**
**Day 4：多模型调用对比**
```python
# huggingface_hub.py
from langchain.llms import HuggingFaceHub
llm_hf = HuggingFaceHub(repo_id="google/flan-t5-xl")
print(llm_hf("Translate to English: 今天天气真好"))
```

**Day 5：动态模板进阶**
```python
# conditional_prompt.py
from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("human", "根据用户描述生成{format}：{input}")
])
chain = prompt | OpenAI()
print(chain.invoke({
    "role": "诗人", 
    "format": "五言绝句",
    "input": "秋天的夜晚"
}))
```

#### **模块2：数据连接（2天）**
**Day 6：PDF文档处理**
```python
# pdf_loader.py
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("report.pdf")
pages = loader.load_and_split()
print(pages[0].page_content[:200])  # 输出第一页前200字符
```

**Day 7：向量数据库实战**
```python
# chroma_db.py
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
docs = [...]  # 加载后的文档列表
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
print(retriever.get_relevant_documents("查询问题"))
```

#### **模块3：Chains与Agents（3天）**
**Day 8：自定义Chain开发**
```python
# custom_chain.py
from langchain.chains import TransformChain
def transform(inputs):
    text = inputs["text"].upper()
    return {"output_text": text}
transform_chain = TransformChain(
    input_variables=["text"], 
    output_variables=["output_text"], 
    transform=transform
)
print(transform_chain.run("hello world"))  # 输出HELLO WORLD
```

**Day 9：Agent工具集成**
```python
# calculator_agent.py
from langchain.agents import load_tools
tools = load_tools(["serpapi", "llm-math"], llm=OpenAI())
from langchain.agents import initialize_agent
agent = initialize_agent(tools, llm, agent="self-ask-with-search", verbose=True)
agent.run("苹果公司当前市值是多少？用人民币表示")
```

#### **模块4：记忆与存储（2天）**
**Day 10：多轮对话实现**
```python
# conversation.py
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
memory.save_context({"input": "你好"}, {"output": "有什么可以帮您？"})
memory.save_context({"input": "推荐一本书"}, {"output": "《人类简史》不错"})
print(memory.load_memory_variables({}))  # 显示完整对话历史
```

---

### **阶段三：实战项目开发（2周）**
#### **项目1：智能文档助手（5天）**
**Day 11-12：PDF解析与向量化**
```python
# pdf_qa.py
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
print(qa.run("论文的主要创新点是什么？"))
```

**Day 13：对话历史增强**
```python
# memory_qa.py
from langchain.chains import ConversationalRetrievalChain
chain = ConversationalRetrievalChain.from_llm(
    OpenAI(), 
    retriever, 
    memory=ConversationBufferMemory()
)
chain({"question": "作者用了什么方法？"}, return_only_outputs=True)
```

#### **项目2：AI客服代理（4天）**
**Day 14：工单系统集成**
```python
# zendesk_integration.py
import requests
def create_ticket(description):
    response = requests.post(
        "https://yourdomain.zendesk.com/api/v2/tickets.json",
        json={"ticket": {"subject": "AI生成工单", "comment": {"body": description}}},
        auth=("email/token", "your_token")
    )
    return response.json()
```

#### **项目3：自动化研究助手（3天）**
**Day 15：文献摘要生成**
```python
# research_summary.py
from langchain.chains.summarize import load_summarize_chain
chain = load_summarize_chain(OpenAI(), chain_type="map_reduce")
with open("paper.txt") as f:
    docs = [Document(page_content=f.read())]
print(chain.run(docs))
```

---

### **执行建议**
1. **每日代码存档**：建立Git仓库，每天提交代码到独立分支
2. **问题记录表**：遇到错误时记录：
   - 错误信息
   - 尝试的解决方案
   - 最终修复方法
3. **可视化进度**：使用Trello看板管理学习任务（Todo/Doing/Done）

**示例学习日程表**：
```
9:00-10:30 理论学习（官方文档+视频教程）
10:45-12:00 代码实践
14:00-15:30 项目开发
16:00-17:00 社区答疑（Discord/Stack Overflow）
```

通过这个计划，您将在 **每天3-4小时** 的学习中系统掌握LangChain开发能力，所有代码示例均可直接运行调试。遇到卡点时，优先查阅官方文档的对应模块说明（按Ctrl+F搜索关键词）。