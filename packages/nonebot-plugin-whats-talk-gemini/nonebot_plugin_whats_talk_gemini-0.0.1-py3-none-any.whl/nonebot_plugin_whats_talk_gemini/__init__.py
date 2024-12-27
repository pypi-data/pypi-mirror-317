import asyncio

import httpx
from nonebot import get_bots, get_plugin_config, on_command, require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from .config import Config

# 插件元数据
__plugin_meta__ = PluginMetadata(
    name="他们在聊什么",
    description="分析群聊记录，生成近期讨论话题的总结。",
    usage=(
        "发送指令“他们在聊什么”或“群友在聊什么”以获取当前群聊的讨论总结。\n"
        "插件会定期自动推送群聊讨论总结，推送时间可配置。"
    ),
    type="application",
    homepage="",
    config=Config,
    supported_adapters={"~onebot.v11"},
)


# 加载插件配置
plugin_config = get_plugin_config(Config)
wt_api_keys = plugin_config.wt_ai_keys
if not wt_api_keys:
    raise ValueError("配置文件中未提供 API Key 列表。")
wt_model_name = plugin_config.wt_model
wt_proxy = plugin_config.wt_proxy
wt_history_lens = plugin_config.wt_history_lens
wt_push_cron = plugin_config.wt_push_cron
wt_group_list = plugin_config.wt_group_list


# 注册事件响应器
whats_talk = on_command(
    "他们在聊什么",
    aliases={"群友在聊什么"},
    priority=5,
    rule=is_type(GroupMessageEvent),
    block=True,
)


# 处理命令
@whats_talk.handle()
async def handle_whats_talk(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    try:
        messages = await get_history_chat(bot, group_id)
        member_count = await get_group_member(bot, group_id)
        if not messages:
            await whats_talk.finish("未能获取到聊天记录。")
        summary = await chat_with_gemini(messages, member_count)
        if not summary:
            await whats_talk.finish("生成聊天总结失败，请稍后再试。")
        await bot.send_group_forward_msg(
            group_id=group_id,
            messages=[
                {
                    "type": "node",
                    "data": {
                        "name": "群聊总结",
                        "uin": bot.self_id,
                        "content": summary,
                    },
                }
            ],
        )
    except Exception as e:
        logger.error(f"命令执行过程中发生错误: {e!s}")
        await whats_talk.finish(f"命令执行过程中发生错误，错误信息: {e!s}")


# 获取群成员数量
async def get_group_member(bot: Bot, group_id: int) -> int:
    try:
        members = await bot.get_group_member_list(group_id=group_id)
        return len(members)
    except Exception as e:
        logger.error(f"获取群成员列表失败: {e!s}")
        return 0


# 获取群聊记录
async def get_history_chat(bot: Bot, group_id: int):
    messages = []
    try:
        history = await bot.get_group_msg_history(
            group_id=group_id,
            count=wt_history_lens,
        )
        for message in history["messages"]:
            sender = message["sender"]["card"] or message["sender"]["nickname"]
            text_messages = [msg["data"]["text"] for msg in message["message"] if msg["type"] == "text"]
            messages.extend([f"{sender}: {text}" for text in text_messages])
    except Exception as e:
        logger.error(f"获取聊天记录失败: {e!s}")
        raise Exception(f"获取聊天记录失败,错误信息: {e!s}")
    return messages


# 调用 AI 接口生成聊天总结
async def chat_with_gemini(messages, member_count):
    prompt = (
        "# Role: 群友聊天总结专家\n"
        "\n"
        "## Profile\n"
        "- author: LangGPT \n"
        "- version: 1.3\n"
        "- language: 中文\n"
        "- description: 你是一名专业的群友聊天总结专家，擅长以话题为单位总结群内的讨论内容，"
        "帮助新来的群友快速了解最近的聊天动态，并通过活跃度、信息熵、话题多样性等多维度提供互动评价，"
        "同时对聊天内容进行全面概括。\n"
        "\n"
        "## Skills\n"
        "1. 按照话题单位划分总结内容，确保逻辑清晰。\n"
        "2. 提取关键信息并以简洁条目形式呈现。\n"
        "3. 突出在讨论中贡献显著或关键用户的内容。\n"
        "4. 量化群内互动情况，包括活跃度、信息熵、话题多样性和讨论深度等。\n"
        "5. 提供对整体聊天内容的全面总结，突出群讨论的主题特点和质量。\n"
        "\n"
        "## Rules\n"
        "1. 将聊天记录归纳为多个话题，并以编号形式呈现。\n"
        "2. 在每个话题中，列出主要讨论内容，标注具有显著贡献的用户。\n"
        "3. 在总结的结尾部分，提供基于以下多维度的互动评价：\n"
        f"   - 活跃人数比例：基于群总人数（{member_count}人），30%（90人）视为最大活跃度，对应5⭐，活跃度按以下标准评分：\n"  # noqa: E501
        "     - ⭐⭐⭐⭐⭐（≥30%），⭐⭐⭐⭐（20%-30%），⭐⭐⭐（10%-20%），⭐⭐（5%-10%），⭐（<5%）\n"
        "   - 信息熵：衡量用户发言内容的分布均衡性，信息熵越高表示讨论越均衡和多样，5⭐表示高度均衡。\n"
        "   - 话题多样性：统计活跃话题数量及其分布，更多高质量话题对应更高评分。\n"
        "   - 深度评分：依据讨论的广度和深度评估，例如是否超越表面问题。\n"
        "4. 在互动评价之后，增加一个整体总结模块，概述聊天内容的主题特点、活跃情况及整体讨论的质量。\n"
        "5. 确保总结条理清晰，重点突出，评价内容准确客观。\n"
        "\n"
        "## Workflows\n"
        "1. 接收聊天记录，解析并归类为不同话题。\n"
        "2. 按话题梳理讨论内容，提炼关键信息。\n"
        "3. 突出对话中的关键用户，标注其参与的具体内容。\n"
        "4. 量化群内互动情况，并按以下方式评估：\n"
        f"   - **活跃人数比例**：统计发言人数与群总人数（{member_count}人）的比值，以30%为5⭐标准线。\n"
        "   - **信息熵**：计算发言频率的分布均衡性，公式为 \\( H = -\\sum (p_i \\cdot \\log_2 p_i) \\)，\\( p_i \\) 为用户发言比例。\n"  # noqa: E501
        "   - **话题多样性**：统计活跃话题数量，并评估各话题的讨论平衡性。\n"
        "   - **深度评分**：分析讨论是否超越基础问题，涉及深入见解或知识拓展。\n"
        "5. 综合量化数据与文字描述，完成以下输出：\n"
        "   - 话题划分与总结。\n"
        "   - 多维度互动评价。\n"
        "   - 整体总结。\n"
        "\n"
        "## OutputFormat\n"
        "1. 每个话题编号呈现，并按以下格式输出：\n"
        "   - **话题编号：话题标题**\n"
        "   - **主要讨论内容**：\n"
        "     - 内容1\n"
        "     - 内容2\n"
        "   - **关键贡献用户**：用户A（贡献内容简述），用户B（贡献内容简述）\n"
        "2. 总结结尾处提供互动评价，格式如下：\n"
        "   - **活跃人数**：{活跃人数}（占群总人数的{比例}%），评分：⭐（{评分依据}）\n"
        "   - **信息熵**：{信息熵值}，评分：⭐（{评分依据}）\n"
        "   - **话题多样性**：{话题数量}，评分：⭐（{评分依据}）\n"
        "   - **深度评分**：⭐（{评分依据}）\n"
        "3. 在互动评价后，增加整体总结模块，格式如下：\n"
        "   - **整体总结**：\n"
        "     - 本次群内讨论主要围绕以下主题展开：{主题概述}。\n"
        "     - 群内整体活跃情况为{活跃评价}，讨论质量{讨论质量评价}。\n"
        "     - 突出特点为：{总结群讨论的特色，例如高效解决问题、多样化话题等}。\n"
        "\n"
        "## 示例\n"
        "**话题1：技术问题讨论**\n"
        "- **主要讨论内容**：\n"
        "  - 内容1\n"
        "  - 内容2\n"
        "- **关键贡献用户**：用户A（描述），用户B（描述）\n"
        "\n"
        "**互动评价**：\n"
        "- **活跃人数**：60人（占群总人数的20%），评分：⭐⭐⭐⭐（活跃度较高）\n"
        "- **信息熵**：3.85，评分：⭐⭐⭐（讨论稍有不均衡）\n"
        "- **话题多样性**：3个话题，评分：⭐⭐⭐⭐（话题较为丰富）\n"
        "- **深度评分**：⭐⭐⭐（讨论深度一般，集中于基础问题）\n"
        "\n"
        "**整体总结**：\n"
        "- 本次群内讨论主要围绕以下主题展开：技术问题解决与经验分享。\n"
        "- 群内整体活跃情况为较高，讨论质量中等偏上。\n"
        "- 突出特点为：快速高效的问题解答，讨论集中但缺乏深入拓展。\n"
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}], "role": "user"},
            {"parts": [{"text": "\n".join(messages)}], "role": "user"},
        ]
    }
    for wt_api_key in wt_api_keys:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{wt_model_name}:generateContent?key={wt_api_key}"
        )
        try:
            async with httpx.AsyncClient(
                proxy=wt_proxy if wt_proxy else None,
                timeout=300,
            ) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=data,
                )
                response.raise_for_status()
                result = response.json()
                content = "".join(
                    item.get("text", "")
                    for item in result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                )
                return content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning(f"API Key {wt_api_key} 已超出限制，切换到下一个 API Key 重试。")
                continue
            else:
                logger.error(f"调用 AI 接口失败: {e!s}")
                raise Exception(f"调用 AI 接口失败，错误信息: {e!s}")
        except Exception as e:
            logger.error(f"发生预料之外的错误: {e!s}")
            raise Exception(f"发生预料之外的错误，错误信息: {e!s}")
    raise Exception("所有 API Key 均超出限制或调用失败。")


# 解析 cron 表达式
def parse_cron_expression(cron: str):
    fields = cron.split()
    if len(fields) != 5:
        raise ValueError(f"无效的 cron 表达式: {cron}")
    minute, hour, day, month, day_of_week = fields
    return {
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week,
    }


# 定时任务
@scheduler.scheduled_job("cron", id="push_whats_talk", **parse_cron_expression(wt_push_cron))
async def push_whats_talk():
    bots = get_bots()
    for bot in bots:
        if isinstance(bot, Bot):
            for group_id in wt_group_list:
                try:
                    messages = await get_history_chat(bot, group_id)
                    member_count = await get_group_member(bot, group_id)
                    if not messages:
                        await bot.send_group_msg(group_id=group_id, message="未能获取到聊天记录。")
                        continue
                    summary = await chat_with_gemini(messages, member_count)
                    if not summary:
                        await bot.send_group_msg(group_id=group_id, message="生成聊天总结失败，请稍后再试。")
                        continue
                    await bot.send_group_forward_msg(
                        group_id=group_id,
                        messages=[
                            {
                                "type": "node",
                                "data": {
                                    "name": "群聊总结",
                                    "uin": bot.self_id,
                                    "content": summary,
                                },
                            }
                        ],
                    )
                except Exception as e:
                    logger.error(f"定时任务处理群 {group_id} 时发生错误: {e!s}")
                    await bot.send_group_msg(
                        group_id=group_id,
                        message=f"命令执行过程中发生错误，错误信息: {e!s}",
                    )
                await asyncio.sleep(2)
