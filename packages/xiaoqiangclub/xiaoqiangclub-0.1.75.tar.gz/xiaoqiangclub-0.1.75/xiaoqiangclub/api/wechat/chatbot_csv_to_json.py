# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/12/19 09:53
# 文件名称： chatbot_csv_to_json.py
# 项目描述： 将Chatbot导出的知识库的csv文件转换为json文件
# 开发工具： PyCharm
import re
import pandas as pd
from typing import Dict, List
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.data.file import write_file_async

# 提取URL的正则表达式
url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'


def modify_ctfile_url(url: str) -> str:
    """
    修改 ctfile.com 的网址，添加查询参数 ?p=xiaoqiangclub。

    :param url: 原始网址
    :return: 修改后的网址
    """
    if "ctfile.com" in url:
        # 如果网址包含 ctfile.com，在网址后加上查询参数
        if "?" not in url:
            url += "?p=xiaoqiangclub"
    return url


def extract_data(file_path: str) -> Dict[str, List[str]]:
    """
    从CSV或Excel文件中提取问题和对应的所有URL，处理 ctfile.com 的URL。

    :param file_path: 输入文件路径，可以是CSV或Excel文件
    :return: 一个字典，键为问题，值为该问题相关的URL列表
    """
    # 获取文件扩展名
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("不支持的文件类型，请提供CSV或Excel文件。")

    # 存储提取后的数据
    result = {}

    # 遍历每一行数据
    for _, row in df.iterrows():
        question = row.get("问题(必填)", "").strip()
        answer = row.get("机器人回答(必填-多个用##分隔)", "").strip()

        # 如果问题不为空，处理回答部分
        if question and answer:
            # 替换 'LINE_BREAK' 为换行符
            answer = answer.replace('LINE_BREAK', '\n')

            # 提取回答中的所有URL
            urls = re.findall(url_pattern, answer)

            # 修改ctfile.com的URL
            modified_urls = [modify_ctfile_url(url) for url in urls]

            # 如果找到了URL，将它们存入字典
            if modified_urls:
                result[question] = modified_urls

    return result


async def chatbot_convert(input_file: str, output_file: str) -> None:
    """
    将chatbot导出的知识库的csv文件转换为json文件。
    https://chatbot.weixin.qq.com/@want26aca/platform/dialogConfig/questionList

    :param input_file: 输入文件路径
    :param output_file: 输出JSON文件路径
    """
    log.info(f"开始处理文件：{input_file}")

    try:
        # 提取数据
        data = extract_data(input_file)

        # 将结果保存到JSON文件
        await write_file_async(output_file, data)
        log.info(f"处理完成，结果已保存到 {output_file}")
    except Exception as e:
        log.error(f"处理过程中出现错误: {e}")


async def chatbot_convert_cli(args) -> None:
    """
    将 Chatbot 导出的知识库 CSV 文件转换为 JSON 文件。
    命令行工具
    """
    input_file = args.input
    output_file = args.output

    await chatbot_convert(input_file, output_file)


if __name__ == '__main__':
    import asyncio


    async def main():
        await chatbot_convert("../test/chatbot_keywords.csv", "../test/chatbot_keywords.json")


    asyncio.run(main())
