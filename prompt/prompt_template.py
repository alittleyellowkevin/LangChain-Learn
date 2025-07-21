from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

# 定义一个提示词模板，包含 adjective 和 content两个模板变量
prompt_template = PromptTemplate.from_template(
    "给我讲一个关于{content}的{adjective}笑话。"
)

# 通过模板参数格式化提示 m模板
result = prompt_template.format(content="猫", adjective="短短的")
print(result)