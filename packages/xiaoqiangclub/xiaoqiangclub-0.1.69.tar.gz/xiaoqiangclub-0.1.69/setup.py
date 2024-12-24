import os
from xiaoqiangclub import VERSION
from setuptools import setup, find_packages


def get_long_description():
    """获取详细描述"""
    try:
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        return 'XiaoqiangClub 自用工具包'
    except Exception as e:
        print(f"读取 README.md 失败: {e}")
        return 'XiaoqiangClub 自用工具包'


setup(
    name='xiaoqiangclub',
    version=VERSION,  # 示例版本号
    author='xiaoqiang',
    author_email='xiaoqiangclub@hotmail.com',
    description='XiaoqiangClub 自用工具包',
    long_description=get_long_description(),  # 项目详细描述
    long_description_content_type='text/markdown',
    url='https://gitee.com/xiaoqiangclub/xiaoqiangclub',
    install_requires=[  # 依赖包
        'aiofiles',
        'aiosqlite',
        'apscheduler',
        'bencodepy',
        'fake_useragent',
        'fastapi',
        'httpx[socks]',
        'jinja2',
        'openai',
        'pandas',
        'parsel',
        'pycryptodome',
        'PyYAML',
        'pyzipper',
        'redis',
        'slowapi',
        'sqlitedict',
        'tinydb',
        'websocket',  # 星火大模型
        'wechatpy',
        'zhipuai'
    ],
    extras_require={
        # pip install xiaoqiangclub[playwright] 安装
        'playwright': ['playwright'],
        # pip install xiaoqiangclub[windows] 安装
        'windows': [
            'pywin32',
            'opencv-python',
            'pillow',
            'PyAutoGUI',
            'pynput',
            'playwright'
        ],
    },
    packages=find_packages(),
    include_package_data=True,  # 确保包含非Python文件
    package_data={
        # 确保模板目录被打包
        'xiaoqiangclub': ['templates/**/*'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='Apache 2.0',  # 指明使用的许可证
    python_requires='>=3.9',
    zip_safe=False,
    entry_points={  # 命令行入口
        'console_scripts': [
            'xiaoqiangclub = xiaoqiangclub.cmd.xiaoqiangclub_cli:main',
        ],
    },
)
