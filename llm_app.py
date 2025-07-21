from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 创建DeepSeek模型实例
llm = ChatOpenAI(
    model_name="deepseek-chat",  # 指定DeepSeek模型名称
    temperature=0,
    openai_api_base="https://api.deepseek.com/v1",  # DeepSeek的API端点
    openai_api_key="sk-dd2f1a07b52545f0854c65d28996273b"  # 替换为你的DeepSeek API密钥
)

# 创建一个字符串输出解析器
output_parser = StrOutputParser()

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的AI技术顾问，请根据用户需求生成相关技术文章。"),
    ("user", "{input}")
])

# 创建链
chain = prompt | llm | output_parser

# 调用链
result = chain.invoke({"input": "帮我写一段AI 的技术文章，100字"})
print(result)