import os
import time

from fastmodels import Client

# 初始化客户端
client = Client(
    api_key="",
    project_id=""
)

# 创建转录任务
create_task_response = client.easyllm.speech_to_text.create(
    easyllm_id="3aKb7l5EXYRFCWUtBhOPmY",
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
