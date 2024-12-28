# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/12/28 11:14
# 文件名称： packaging_app.py
# 项目描述： 打包app
# 开发工具： PyCharm
import os
from xiaoqiangclub.cmd.terminal_command_executor import run_command


def packaging_app(script_path: str,
                  app_title: str,
                  version: str = "v0.0.1",
                  logo_path: str = None,
                  upx_dir: str = None,
                  create_single_file: bool = True,
                  with_cmd_window: bool = False):
    """
    通用打包函数，将 Python 脚本打包为可执行文件，并增加反编译保护措施。
    使用 pip install -i https://mirrors.aliyun.com/pypi/simple/ -U pyinstaller 安装 PyInstaller。
    upx下载:https://github.com/upx/upx/releases/

    :param script_path: 要打包的 Python 脚本路径
    :param app_title: 应用程序名称
    :param version: 应用程序版本
    :param logo_path: 应用程序图标路径，默认为 None（即不设置图标）
    :param upx_dir: UPX 的安装路径（如果使用 UPX 进行加壳）
    :param create_single_file: 是否生成单文件可执行文件，默认为 True
    :param with_cmd_window: 是否显示命令行窗口，默认为 False（即不显示）
    """
    # 选择是否显示命令行窗口
    win_option = '' if with_cmd_window else '-w'

    # UPX 加壳选项
    upx_option = f'--upx-dir={upx_dir}' if upx_dir else ''

    # 设置图标选项
    logo_option = f'-i {logo_path}' if logo_path else ''

    # 单文件或多文件版本
    single_file_option = '--onefile' if create_single_file else ''

    # 构建 PyInstaller 命令
    command = f'pyinstaller {win_option} --name {app_title}{version} {logo_option} {script_path} {upx_option} {single_file_option}'

    # 执行打包命令
    run_command(command)

    # 打开生成的文件所在目录
    open_dir = os.path.join(os.getcwd(), 'dist')
    os.startfile(open_dir)
