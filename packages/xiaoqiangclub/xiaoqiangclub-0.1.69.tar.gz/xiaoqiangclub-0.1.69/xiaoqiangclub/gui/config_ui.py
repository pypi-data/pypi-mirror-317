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
from starlette.responses import RedirectResponse
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.config.constants import ROOT_PATH
from xiaoqiangclub.data.file import (read_file_async, write_file_async)


def generate_config_ui(default_config_file: str,
                       app: FastAPI = None,
                       user_config_dir_or_file: str = None,
                       route_path: str = "/",
                       redirect_if_not_found: bool = True,
                       generate_readme: bool = False) -> FastAPI:
    """
    向现有 FastAPI 应用中添加应用配置页面路由，也可直接使用。
    使用说明文档路径：xiaoqiangclub/templates/html/config_template/config_ui_readme.md

    :param default_config_file: 配置文件路径：用于设置配置页面的控件布局和默认参数，必须是 JSON 和 YAML 文件。
    :param user_config_dir_or_file: 用户的配置数据存放的目录路径/文件，程序会将用户的配置数据存放在该目录下名为 user_config 后缀和 default_config_file 相同的文件中，如果为 None，程序会在当前目录下自动创建一个 "data" 目录
    :param app: 将应用添加到现有的 FastAPI 应用，如果为 None，程序会自动创建一个 FastAPI 应用
    :param route_path: 配置页面的路由路径，默认为 "/"
    :param redirect_if_not_found: 是否将不存在的配置页面重定向到默认配置页面，默认为 True
    :param generate_readme: 是否复制默认的 config_ui_readme.md 文件到 data_dir 目录下，默认为 False
    """
    # 判断 default_config_file 是否是 JSON 和 YAML 文件。
    if not default_config_file.endswith((".json", ".yaml", ".yml")):
        log.error("default_config_file 必须是 JSON 或 YAML 文件")
        raise ValueError("default_config_file 必须是 JSON 或 YAML 文件")

    user_config_file_suffix = os.path.splitext(default_config_file)[1]  # 获取 default_config_file 配置文件的后缀

    # 初始化配置目录和文件
    if user_config_dir_or_file:
        if user_config_dir_or_file.endswith((".json", ".yaml", ".yml")):  # 如果是文件路径
            config_dir = os.path.dirname(user_config_dir_or_file)
            # 将 user_config_dir_or_file 文件的后缀改为 default_config_file 相同
            user_config_file = os.path.splitext(user_config_dir_or_file)[0] + user_config_file_suffix

        else:  # 如果是目录路径
            config_dir = user_config_dir_or_file
            user_config_file = os.path.join(config_dir, f"user_config{user_config_file_suffix}")

    else:  # 未提供路径，使用默认目录
        config_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(config_dir, exist_ok=True)
        user_config_file = os.path.join(config_dir, f"user_config{user_config_file_suffix}")

    # 是否生成 README 文件
    if generate_readme:
        readme_file = os.path.join(config_dir, "config_ui_readme.md")
        if not os.path.exists(readme_file):
            log.info(f"生成 config_ui_readme.md 到目录：{config_dir}")
            shutil.copy(os.path.join(ROOT_PATH, 'templates/html/config_template/config_ui_readme.md'), readme_file)

    # 如果没有传入 app，创建一个默认的 FastAPI 应用
    if not app:
        app = FastAPI()

    config_page_templates = Jinja2Templates(
        directory=os.path.join(ROOT_PATH, 'templates/html/config_template/templates'))

    async def sort_dict_by_order(dict_data: Dict[str, Any]) -> Dict[str, Any]:
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

    @app.get(route_path, response_class=HTMLResponse)
    async def get_settings_page(request: Request):
        """配置页面"""
        # 如果没有用户配置文件，则从默认配置文件中复制内容
        if not os.path.exists(user_config_file):
            os.makedirs(config_dir, exist_ok=True)  # 确保目录存在

            if not os.path.exists(default_config_file):
                log.error(f"默认配置文件不存在：{default_config_file}")
                raise FileNotFoundError(f"默认配置文件不存在：{default_config_file}")

            shutil.copy(default_config_file, user_config_file)
            log.info(f"已复制默认配置文件到：{user_config_file}")

        settings = await read_file_async(user_config_file)
        return config_page_templates.TemplateResponse("config_ui.html",
                                                      {"request": request, "settings": settings})

    @app.get("/{path:path}")
    async def catch_all(path: str):
        """未匹配到路由，重定向到主页"""
        if redirect_if_not_found:  # 检查是否启用重定向
            log.info(f"未匹配到路由，重定向到主页：/{path} >>> {route_path}")
            return RedirectResponse(url=route_path)
        else:
            log.info(f"未匹配到路由且未启用重定向：/{path}")
            return {"error": "Path not found", "requested_path": path}

    @app.post("/config/save_settings")
    async def save_settings(user_settings: dict):
        """保存配置"""
        settings = await sort_dict_by_order(user_settings)
        await write_file_async(user_config_file, settings)
        return {"status": "success", "message": "设置已保存！"}

    @app.post("/config/reset_settings")
    async def reset_settings():
        """重置配置"""
        initial_config = await read_file_async(default_config_file)
        await write_file_async(user_config_file, initial_config)
        return {"status": "success", "message": "设置已恢复为初始状态！"}

    return app
