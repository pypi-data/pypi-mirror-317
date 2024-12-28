# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/12/18 16:26
# 文件名称： config_ui.py
# 项目描述： 一个快速简便生成配置页面的工具
# 开发工具： PyCharm
import os
import shutil
from typing import (Dict, Any)
from fastapi import (FastAPI, Request)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from xiaoqiangclub.config.log_config import log
from starlette.responses import RedirectResponse
from xiaoqiangclub import (read_file_async, write_file_async)

# [自定义]配置文件路径：用于设置配置页面的控件布局和默认参数，必须是 JSON 和 YAML 文件。
default_config_file = "config_ui.json"

# 当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")

# 生成和 default_config_file 相同后缀的 user_config_file
user_config_file_suffix = os.path.splitext(default_config_file)[1]
user_config_file = os.path.join(data_dir, f"default_config{user_config_file_suffix}")

app = FastAPI()

# 模板渲染器
templates = Jinja2Templates(directory="templates")


async def config_ui_sort(dict_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    对字典进行排序，外层字典按顺序排列，内层字典根据 'order' 字段进行排序。

    :param dict_data: 需要排序的字典数据，字典的键为字符串，值可以是任何类型
    :return: 排序后的字典，外层字典按顺序排列，内层字典中的元素按 'order' 字段排序
    """
    first_order = []  # 存储外层字典的排序顺序
    dict_map = []  # 存储内层字典的排序信息

    # 处理外层字典
    for key, value in dict_data.items():
        if isinstance(value, dict):
            orders = []  # 存储内层字典中 'order' 的值
            second_order = []  # 存储内层字典的排序顺序

            # 获取内层字典的 'order' 值并排序
            for inner_key, inner_value in value.items():
                # 确保 inner_value 是字典类型
                if isinstance(inner_value, dict):
                    orders.append(int(inner_value.get('order', float('inf'))))  # 如果没有 'order'，设为无限大
                else:
                    orders.append(float('inf'))  # 如果不是字典，设为无限大

            # 对 'order' 值进行排序，并按排序后的顺序将键添加到 second_order
            sorted_inner_order = sorted(orders)
            for i in sorted_inner_order:
                for inner_key, inner_value in value.items():
                    if isinstance(inner_value, dict) and i == inner_value.get('order', float('inf')):
                        second_order.append(inner_key)

            dict_map.append((key, sorted_inner_order[0], second_order))  # 记录外层字典的排序信息
        else:
            # 如果是普通字段（如 'title', 'logo'），直接添加到 first_order
            first_order.append(key)

    # 根据内层字典的 'order' 字段排序外层字典
    orders = [data[1] for data in dict_map]  # 获取排序的 'order' 值
    sorted_first_order = sorted(orders)  # 排序所有内层字典的 'order'

    # 将排序后的内层字典添加到 first_order 中
    for i in sorted_first_order:
        for data in dict_map:
            if data[1] == i:
                first_order.append(data)

    # 构建新的排序后的字典
    new_dict = {}
    for data in first_order:
        if isinstance(data, str):
            # 如果是普通字段，直接添加到新字典
            new_dict[data] = dict_data[data]
        elif isinstance(data, tuple):
            # 如果是包含字典的字段，按照排序后的顺序添加
            new_dict[data[0]] = {}
            for inner_key in data[2]:
                new_dict[data[0]][inner_key] = dict_data[data[0]][inner_key]

    return new_dict


@app.get("/", response_class=HTMLResponse)
async def get_settings_page(request: Request):
    """配置页面"""
    # 如果没有用户配置文件，则从默认配置文件中复制内容
    if not os.path.exists(user_config_file):
        if not os.path.exists(default_config_file):
            log.error(f"默认配置文件不存在：{default_config_file}")
            raise FileNotFoundError(f"默认配置文件不存在：{default_config_file}")
        shutil.copy(default_config_file, user_config_file)
        log.info(f"已复制默认配置文件到：{user_config_file}")

    settings = await read_file_async(user_config_file)  # 读取当前配置
    return templates.TemplateResponse("config_ui.html",
                                      {"request": request, "settings": settings})


@app.post("/config/save_settings")
async def save_settings(user_settings: dict):
    """保存修改的配置"""

    settings = await config_ui_sort(user_settings)
    await write_file_async(user_config_file, settings)  # 保存更新后的配置

    return {"status": "success", "message": "设置已保存！"}


@app.post("/config/reset_settings")
async def reset_settings():
    """重置配置"""
    # 读取初始配置
    initial_config = await read_file_async(default_config_file)  # 假设config_file是初始设置的文件

    # 重新写入初始配置到 user_config.json
    await write_file_async(user_config_file, initial_config)

    return {"status": "success", "message": "设置已恢复为初始状态！"}


@app.get("/{path:path}")
async def catch_all(path: str):
    """未匹配到路由，重定向到主页，注意：这条路由必须在末尾，否则会被其他路由拦截"""
    log.info(f"未匹配到路由，重定向到主页：{path} >>> /")
    return RedirectResponse(url="/")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
