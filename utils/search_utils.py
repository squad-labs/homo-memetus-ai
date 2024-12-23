import os
import asyncio
import requests
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from datetime import datetime

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["SERP_API_KEY"] = os.getenv('SERP_API_KEY')
os.environ['SEARCH_MODEL_ID'] = os.getenv("SEARCH_MODEL_ID")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
SERP_API_KEY = os.environ["SERP_API_KEY"]
SEARCH_MODEL_ID = os.environ["SEARCH_MODEL_ID"]

load_dotenv()

class TavilySearchResults(TypedDict):
  messages: Annotated[list, add_messages]

repl = PythonREPL()

def python_repl(
  code: Annotated[str, "The python code to execute to generate your chart."],
):
  """Use this to execute python code. If you want to see the output of a value,
  you should print it out with `print(...)`. chart labels should be written in English.
  This is visible to the user."""
  try:
      result = repl.run(code)
  except BaseException as e:
      return f"Failed to execute. Error: {repr(e)}"
  result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
  return (
      result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
  )

def get_serp_results():
  url = f"https://serpapi.com/search.json?engine=google_news&q=btc&api_key={SERP_API_KEY}"
  try:
    res = requests.get(url)
    data = res.json()['news_results']
    simplified_news = []

    for news_item in data:
      if 'stories' in news_item:
        for story in news_item['stories']:
          timestamp = int(datetime.strptime(story['date'], '%m/%d/%Y, %H:%M %p, %z %Z').timestamp() * 1000)
          simplified_news.append((story['title'], story.get('source', {}).get('name', 'Unknown source'), timestamp))
      else:
        if news_item.get('date'):
          timestamp = int(datetime.strptime(news_item['date'], '%m/%d/%Y, %H:%M %p, %z %Z').timestamp() * 1000)
          simplified_news.append((news_item['title'], news_item.get('source', {}).get('name', 'Unknown source'), timestamp))
        else:
          simplified_news.append((news_item['title'], news_item.get('source', {}).get('name', 'Unknown source'), 'No timestamp provided'))
    result = str(simplified_news)
  except Exception as e:
    return f"Failed to get search results. Error: {repr(e)}"
  return result

def get_tavily_results():
  web_search = TavilySearchResults(max_results=5)
  return web_search

tools=[get_tavily_results, get_serp_results, python_repl]
tool_node = ToolNode(tools)

llm = ChatOpenAI(model=f"{SEARCH_MODEL_ID}")
llm_with_tools = llm.bind_tools(tools)

def agent(state: TavilySearchResults):
  result = llm_with_tools.invoke(state["messages"])
  return {"messages": [result]}

def should_continue(state):
  messages = state["messages"]
  last_message = messages[-1]
  if not last_message.tool_calls:
    return "end"
  else:
    return "continue"
    
workflow = StateGraph(TavilySearchResults)

workflow.add_node("agent", agent)
workflow.add_node("tool", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
  "agent",
  should_continue,
  {
    "continue": "tool",
    "end": END,
  },
)

workflow.add_edge("tool", "agent")

memory = MemorySaver()

graph = workflow.compile(checkpointer=memory, interrupt_before=["tool"])

display(Image(graph.get_graph().draw_mermaid_png()))

initial_input = {"messages": [HumanMessage(content="Can you recommend notable meme coins to watch for in Q4 2024 and Q1 2025?")]}

async def process_graph_updates(graph, initial_input, stream_mode="updates"):
  thread = {"configurable": {"thread_id": str(1)}}
  async for chunk in graph.astream(initial_input, thread, stream_mode=stream_mode):
    for node, values in chunk.items():
      print(f"Receiving update from node: '{node}'" )
      print(values)
      print("\n\n")

