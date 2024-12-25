from fastmodels import Client

# 初始化客户端
client = Client(
    api_key="",
    project_id=""
)
stream = True
# 调用接口
response = client.chat.completions.create(
    model_id="",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁"},
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
