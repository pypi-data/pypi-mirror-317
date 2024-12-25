import json
from langchain_openai import ChatOpenAI
from .agent import run_agent, Runnable, output, CHAT_DATA, clear_chat_data
import asyncio
from pycoze import utils
from pycoze.reference.bot import ref_bot
from pycoze.reference.tool import ref_tools
from pycoze.reference.workflow import ref_workflow
from langchain_core.utils.function_calling import convert_to_openai_tool
import os

cfg = utils.read_json_file("llm.json")


def load_role_setting(bot_setting_file: str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_abilities(bot_setting_file: str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        role_setting = json.load(f)

    abilities = []
    for bot_id in role_setting["bots"]:
        bot = ref_bot(bot_id, as_agent_tool=True)
        if bot:
            abilities.append(bot)
    for tool_id in role_setting["tools"]:
        abilities.extend(ref_tools(tool_id, as_agent_tool=True))
    for workflow_id in role_setting["workflows"]:
        workflow = ref_workflow(workflow_id, as_agent_tool=True)
        if workflow:
            abilities.append(workflow)
    return abilities


async def check_interrupt_file(interval, interrupt_file,agent_task):
    while True:
        await asyncio.sleep(interval)
        if os.path.exists(interrupt_file):
            os.remove(interrupt_file)
            agent_task.cancel()
            break 
        
async def run_with_interrupt_check(agent, history, interrupt_file, check_interval=1):
    clear_chat_data()
    try:
        agent_task = asyncio.create_task(run_agent(agent, history))
        check_task = asyncio.create_task(check_interrupt_file(check_interval, interrupt_file, agent_task))
        result = await agent_task
        return result
    except asyncio.CancelledError:
        return CHAT_DATA['info']
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return None  # 返回 None 或者处理异常后的结果
    finally:
        if not agent_task.done():
            agent_task.cancel()
        # 确保即使发生异常也会取消检查任务
        if not check_task.done():
            check_task.cancel()
            try:
                await check_task
            except asyncio.CancelledError:
                pass  # 忽略取消错误

async def agent_chat(bot_setting_file, history):
    role_setting = load_role_setting(bot_setting_file)
    abilities = load_abilities(bot_setting_file)

    chat = ChatOpenAI(
        api_key=cfg["apiKey"],
        base_url=cfg["baseURL"],
        model=cfg["model"],
        temperature=(
            role_setting["temperature"] * 2
            if cfg["model"].startswith("deepseek")
            else role_setting["temperature"]
        ),
        stop_sequences=[
            "tool▁calls▁end",
            "tool▁call▁end",
        ],  # 停用deepseek的工具调用标记，不然会虚构工具调用过程和结果
    )
    prompt = role_setting["prompt"]

    agent = Runnable(
        agent_execution_mode="FuncCall",
        tools=abilities,
        llm=chat,
        assistant_message=prompt,
    )
    params = utils.read_params_file()
    if "interruptFile" in params:
        interrupt_file_path = params["interruptFile"]
        result = await run_with_interrupt_check(agent, history,interrupt_file_path)
    else:
        result = await run_agent(agent, history)
    return result

