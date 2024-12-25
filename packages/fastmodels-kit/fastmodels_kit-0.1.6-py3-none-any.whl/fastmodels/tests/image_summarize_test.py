import os
from fastmodels import Client

# 初始化客户端
client = Client(
    api_key="",
    project_id=""
)
stream = True
# 调用接口
response = client.easyllm.image_summarize.create(
    easyllm_id="",
    image_url="",
    stream=stream,
)

# 打印输出
if stream:
    for chunk in response:
        for choice in chunk.choices:
            print(f"Index: {choice.index}, Content: {choice.delta.content}, Finish Reason: {choice.finish_reason}")
else:
    print(response.choices[0].message.content)
