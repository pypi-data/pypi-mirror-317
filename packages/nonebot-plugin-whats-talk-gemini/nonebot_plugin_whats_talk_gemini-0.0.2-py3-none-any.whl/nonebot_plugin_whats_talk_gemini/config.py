from typing import List  # noqa: UP035

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    wt_ai_keys: List[str] = []  # AI 接口密钥列表
    wt_model: str = "gemini-2.0-flash-exp"  # AI 模型名称
    wt_proxy: str = ""  # 代理设置
    wt_history_lens: int = 1000  # 获取历史消息的数量
    wt_push_cron: str = "0 14,22 * * *"  # 定时任务的 cron 表达式
    wt_group_list: List[int] = []  # 定时推送的群组列表
