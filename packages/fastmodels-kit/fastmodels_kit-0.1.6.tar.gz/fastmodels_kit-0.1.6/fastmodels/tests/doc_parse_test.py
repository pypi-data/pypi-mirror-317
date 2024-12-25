# -*- coding: utf-8 -*-

from fastmodels import Client

# 初始化客户端
client = Client(
    api_key="",
    project_id=""
)

# 打开文件
file_path = 'D:\考试资料\复盘模型.docx'  # 替换为您的文件路径

with open(file_path, 'rb') as file:
    response = client.easyllm.doc_parse.create(
        easyllm_id="3JLhihlJ6RdCyjCrRYZ6Vw",
        file_path=file_path
    )

# 打印输出
print(response.data)
