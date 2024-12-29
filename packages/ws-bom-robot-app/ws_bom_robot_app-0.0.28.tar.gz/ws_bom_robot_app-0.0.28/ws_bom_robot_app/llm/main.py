from typing import  AsyncGenerator
from ws_bom_robot_app.llm.agent_lcel import AgentLcel
from ws_bom_robot_app.llm.agent_handler import AgentHandler, RawAgentHandler
from ws_bom_robot_app.llm.agent_description import AgentDescriptor
from langchain_core.messages import HumanMessage, AIMessage
from ws_bom_robot_app.llm.tools.tool_builder import get_structured_tools
from ws_bom_robot_app.llm.models.api import InvokeRequest, StreamRequest
import ws_bom_robot_app.llm.settings as settings
from nebuly.providers.langchain import LangChainTrackingHandler
from langchain_core.callbacks.base import AsyncCallbackHandler
import warnings, asyncio, os, io, sys, json
from typing import List
from asyncio import Queue
from langchain.callbacks.tracers import LangChainTracer
from langsmith import Client as LangSmithClient

async def invoke(rq: InvokeRequest) -> str:
  await rq.initialize()
  _msg: str = rq.messages[-1].content
  processor = AgentDescriptor(api_key=rq.secrets["openAIApiKey"],
      prompt=rq.system_message,
      mode = rq.mode,
      rules=rq.rules if rq.rules else None
  )
  result: AIMessage = await processor.run_agent(_msg)
  return {"result": result.content}

async def __stream(rq: StreamRequest,queue: Queue,formatted: bool = True) -> None:
  await rq.initialize()
  #os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
  if formatted:
    agent_handler = AgentHandler(queue,rq.thread_id)
  else:
    agent_handler = RawAgentHandler(queue)
  os.environ["AGENT_HANDLER_FORMATTED"] = str(formatted)
  callbacks: List[AsyncCallbackHandler] = [agent_handler]
  settings.init()

  #CREATION OF CHAT HISTORY FOR AGENT
  for message in rq.messages:
      if message.role == "user":
          settings.chat_history.append(HumanMessage(content=message.content))
      elif message.role == "assistant":
          message_content = ""
          if '{\"type\":\"string\"' in message.content:
            try:
              json_msg = json.loads('[' + message.content[:-1] + ']')
              for msg in json_msg:
                if msg.get("content"):
                  message_content += msg["content"]
            except:
              message_content = message.content
          else:
            message_content = message.content
          settings.chat_history.append(AIMessage(content=message_content))

  if rq.lang_chain_tracing:
    client = LangSmithClient(
      api_key= rq.secrets.get("langChainApiKey", "")
    )
    trace = LangChainTracer(project_name=rq.lang_chain_project,client=client)
    callbacks.append(trace)

  processor = AgentLcel(
      openai_config={"api_key": rq.secrets["openAIApiKey"], "openai_model": rq.model, "temperature": rq.temperature},
      sys_message=rq.system_message,
      tools=get_structured_tools(tools=rq.app_tools, api_key=rq.secrets["openAIApiKey"], callbacks=[callbacks], queue=queue),
      rules=rq.rules
  )
  if rq.secrets.get("nebulyApiKey","") != "":
    nebuly_callback = LangChainTrackingHandler(
            api_key= rq.secrets.get("nebulyApiKey"),
            user_id=rq.thread_id,
            nebuly_tags={"project": rq.lang_chain_project},
        )
    callbacks.append(nebuly_callback)

  with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)

    await processor.executor.ainvoke(
        {"input": rq.messages[-1], "chat_history": settings.chat_history},
        {"callbacks": callbacks},
    )

  # Signal the end of streaming
  await queue.put(None)

async def stream(rq: StreamRequest,formatted:bool = True) -> AsyncGenerator[str, None]:
    queue = Queue()
    task = asyncio.create_task(__stream(rq, queue, formatted))
    try:
        while True:
            token = await queue.get()
            if token is None:  # None indicates the end of streaming
                break
            yield token
    finally:
        await task

async def stream_none(rq: StreamRequest, formatted: bool = True) -> None:
  await __stream(rq, formatted)
