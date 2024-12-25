# FastModels Python Library

Open Platform提供了Python SDK，帮助开发者能够高效且便捷地集成和调用API，只需几行代码即可轻松接入大模型能力。

## 环境准备
### 前置条件
1. 完成项目创建、API Key创建、启用服务之后，才能调用服务端 API
2. 调用 API 时，需要将访问凭证放入请求 Header 中（Authorization:Bearer <API Key>）。
3. Open Platform提供的 API 遵循 RESTful 风格，路径参数PROJECT_ID和body参数MODEL_ID可以在项目概览页复制获取

### Installation
要安装FastModels Python库，请运行以下命令：

```sh
pip install fastmodels-kit
```

## 设置环境变量
```sh
setx API_KEY "REPLACE_WITH_YOUR_KEY_VALUE_HERE" 

setx PROJECT_ID "REPLACE_WITH_YOUR_PROJECT_ID_HERE" 
```
## Python Library Usage Example code

您还可以直接在Python代码中使用FastModels Python库。以下是简单使用示例：
### Chat Completions

```python
import os
from fastmodels import Client

# 初始化客户端
client = Client(
    api_key=os.getenv("API_KEY"),
    project_id=os.getenv("PROJECT_ID")
)
stream = True
# 调用接口
response = client.chat.completions.create(
    model_id="REPLACE_WITH_YOUR_MODEL_ID_HERE",
    messages=[
        {"role": "system", "content": "你是LLMOP智能助手"},
        {"role": "user", "content": "你可以帮我做些什么"},
    ],
    stream=stream
)

# 打印输出
if stream:
    for chunk in response:
        for choice in chunk.choices:
            print(f"Index: {choice.index}, Content: {choice.delta.content}, Finish Reason: {choice.finish_reason}")
else:
    print(response.choices[0].message.content)
```

### Image Summarize

```python
import os
from fastmodels import Client

# 初始化客户端
client = Client(
    api_key=os.getenv("API_KEY"),
    project_id=os.getenv("PROJECT_ID")
)
stream = False
# 调用接口
response = client.easyllm.image_summarize.create(
    easyllm_id="REPLACE_WITH_YOUR_EASYLLM_ID_HERE",
    image_url="https://img2.baidu.com/it/u=2772977033,4022698311&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=702",
    stream=stream,
)

# 打印输出
if stream:
    for chunk in response:
        for choice in chunk.choices:
            print(f"Index: {choice.index}, Content: {choice.delta.content}, Finish Reason: {choice.finish_reason}")
else:
    print(response.choices[0].message.content)
```

### Speech To Text

```python
import os
import time

from fastmodels import Client

# 初始化客户端
client = Client(
    api_key=os.getenv("API_KEY"),
    project_id=os.getenv("PROJECT_ID")
)

# 创建转录任务
create_task_response = client.easyllm.speech_to_text.create(
    easyllm_id="REPLACE_WITH_YOUR_EASYLLM_ID_HERE",
    audio_url="",

)
# 最大轮询次数为10次
max_retries = 10
current_retry = 0

# 轮询间隔时间为3秒
retry_interval = 3

while current_retry < max_retries:
    # 获取任务状态
    task = client.easyllm.speech_to_text.get(create_task_response.task_id)

    # 检查任务状态
    if task.status == "success":
        # 如果任务成功，则取出结果并退出循环
        meeting_transcript = task.result
        print("转录结果：" + meeting_transcript)
        break
    elif task.status == "failed":
        # 如果任务失败，则可以选择退出或记录错误
        print("任务失败，无法获取结果")
        break
    else:
        # 如果任务还在进行中，等待指定的重试间隔后再次检查
        print("任务处理中，等待一段时间后重试查询")
        time.sleep(retry_interval)
        current_retry += 1

# 检查是否超出重试次数
if current_retry == max_retries:
    print("已达到最大重试次数，任务仍未完成")
```
### Meeting Minutes

```python
import os
from fastmodels import Client

# 初始化客户端
client = Client(
    api_key=os.getenv("API_KEY"),
    project_id=os.getenv("PROJECT_ID")
)

stream = True
meeting_minutes_response = client.easyllm.meeting_minutes.create(
    easyllm_id="",
    meeting_transcript="",
    stream=stream,

)

# 打印输出
if stream:
    for chunk in meeting_minutes_response:
        for choice in chunk.choices:
            print(f"Index: {choice.index}, Content: {choice.delta.content}, Finish Reason: {choice.finish_reason}")
else:
    print(meeting_minutes_response.choices[0].message.content)
```

