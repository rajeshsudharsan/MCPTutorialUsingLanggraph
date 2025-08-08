
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.graph import MessagesState,StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import create_react_agent


load_dotenv()

SECRET_PATH = os.getenv("SECRET_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SYSTEM_MESSAGE = "You are an useful Assistant that can help with tasks including calendar management. Please complete the tasks using the tools provided and responsd with 'END' when done"

llm = ChatOpenAI(
    model_name="o4-mini-2025-04-16",
    openai_api_key=OPENAI_API_KEY
)


client = MultiServerMCPClient(
    {
        "google_calendar_server": {
            "command": "npx",
            "args": ["-y","mcp-google-calendar"],
            "env": {'CREDENTIALS_PATH':SECRET_PATH},
            "transport":"stdio"
        }
    }
) 

tools = asyncio.run(client.get_tools())

for tool in tools:
    print(f"Tool: {tool.name} - {tool.description}")

model_with_tools = llm.bind_tools(tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    print('should_continue',last_message.content)
    if "END" in last_message.content:
        print('Returning END from should_continue')
        return END
    return "tools"

# Define call_model function
def call_model(state: MessagesState):
    
    if(len(state["messages"]) == 1):
        messages = [SYSTEM_MESSAGE] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    else:
        return {"messages":["END"]}

async def main():
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools",ToolNode(tools))

    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        should_continue,
    )

    builder.add_edge("tools","call_model")
    
    # Compile the graph
    graph = builder.compile()

    response = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "Create a Calendar event on 08/11/2025 for Work"}]}, {"recursion_limit": 5}
    )

    print('Final Response:', response["messages"][-2].content)
    print('Final Response Done')

try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")