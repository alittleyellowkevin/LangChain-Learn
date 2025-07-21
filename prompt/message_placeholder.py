# 导入ChatPromptTemplate和MessagesPlaceholder用于构建聊天提示模板
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# 导入HumanMessage用于表示用户消息
from langchain_core.messages import HumanMessage

# 创建一个聊天提示模板，包含系统消息和消息占位符
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

# 调用模板，将一条用户消息传入msgs占位符
result = prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
# 打印结果
print(result)