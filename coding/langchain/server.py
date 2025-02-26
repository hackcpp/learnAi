from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv
import os

load_dotenv()

key = getenv("SF_API_KEY") 
url = getenv("SF_API_BASE")
model = getenv("SF_MODEL")

os.environ["DEEPSEEK_API_KEY"] = key
os.environ["DEEPSEEK_API_BASE"] = url
# print(key, url, model)

class Args(BaseModel):
    text: str
    language: str

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatDeepSeek(
    model=model,
    temperature=0,
    max_retries=2,
    # other params...
)

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser

# 4. App definition
app = FastAPI()

@app.post("/solve")
async def solve_problem(args: Args):
    return {"solution": await chain.ainvoke(args.model_dump())}
