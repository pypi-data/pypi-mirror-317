# reference：https://github.com/maxtheman/opengpts/blob/d3425b1ba80aec48953a327ecd9a61b80efb0e69/backend/app/agent_types/openai_agent.py
import json

from langchain.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.language_models.base import LanguageModelLike
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import END
from langgraph.graph.message import MessageGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation
import re
import json
import random
from .const import HumanToolString

def get_all_markdown_json(content):
    # Find all markdown json blocks
    markdown_json_blocks = re.findall(r"```json(.*?)```", content, re.DOTALL)
    json_list = []

    for block in markdown_json_blocks:
        try:
            # Remove any leading/trailing whitespace and parse the JSON
            json_data = json.loads(block.strip())
            json_list.append(json_data)
        except json.JSONDecodeError:
            # If the block is not valid JSON, skip it
            continue

    return json_list


def get_tools(last_message):
    if "tool_calls" in last_message.additional_kwargs:
        return last_message.additional_kwargs["tool_calls"]
    else:
        return None


def create_openai_func_call_agent_executor(
    tools: list[BaseTool],
    llm: LanguageModelLike,
    system_message: str,
    **kwargs
):

    async def _get_messages(messages):
        msgs = []
        for m in messages:
            if isinstance(m, ToolMessage):
                _dict = m.dict()
                _dict["content"] = str(_dict["content"])
                m_c = ToolMessage(**_dict)
                msgs.append(m_c)
            else:
                msgs.append(m)

        return [SystemMessage(content=system_message)] + msgs

    if tools:
        llm_with_tools = llm.bind(tools=[convert_to_openai_tool(t) for t in tools])
    else:
        llm_with_tools = llm
    agent = _get_messages | llm_with_tools
    tool_executor = ToolExecutor(tools)

    # Define the function that determines whether to continue or not
    def should_continue(messages):
        # If there is no FuncCall, then we finish
        last_message = messages[-1]
        if last_message.content.strip().endswith("```"):
            last_message.content = last_message.content + "\n\n"  # 避免影响阅读
        tools = get_tools(last_message)
        if last_message.tool_calls or tools:
            return 'continue'
        return 'end'

        

    # Define the function to execute tools
    async def call_tool(messages):
        actions: list[ToolInvocation] = []
        # Based on the continue condition
        # we know the last message involves a FuncCall
        last_message = messages[-1]
        for tool_call in get_tools(last_message):
            function = tool_call["function"]
            function_name = function["name"]

            _tool_input = json.loads(function["arguments"] or "{}")
            # We construct an ToolInvocation from the function_call
            actions.append(
                ToolInvocation(
                    tool=function_name,
                    tool_input=_tool_input,
                )
            )
        # We call the tool_executor and get back a response
        responses = await tool_executor.abatch(actions, **kwargs)
        # We use the response to create a ToolMessage
        tool_messages = []
        for tool_call, response in zip(
            get_tools(last_message), responses
        ):
            if not isinstance(response, (str, int, float, bool, list, tuple)):
                response = repr(
                    response
                )  # 不支持其他类型，包括dict也不支持，因此需要转换为字符串

            message = ToolMessage(
                tool_call_id=tool_call["id"],
                content=response,
                additional_kwargs={"name": tool_call["function"]["name"]},
            )
            tool_messages.append(message)

        return tool_messages

    workflow = MessageGraph()

    # Define the two nodes we will cycle between
    workflow.add_node("agent", agent)
    workflow.add_node("call_tool", call_tool)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "call_tool",
            "end": END,
        },
    )

    # 调用完工具后，再次调用agent
    workflow.add_edge("call_tool", "agent")

    return workflow.compile()
