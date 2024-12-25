import os
from typing import Any, List, Dict, Union, Generator, Optional

import requests

from fastmodels.response_params import CreateTranscriptionResponse, ChatCompletionResponse, \
    ChatCompletionChunk, parse_chat_stream, GetTranscriptionResponse, parse_agent_stream, AgentCompletionChunk, \
    AgentCompletionResponse, DocParseResponse


class Client:
    def __init__(self, api_key=None, project_id=None):
        self.api_key = api_key or os.getenv("API_KEY")
        self.project_id = project_id or os.getenv("PROJECT_ID")
        self.chat = ChatClient(self.api_key, self.project_id)
        self.agent = AgentClient(self.api_key, self.project_id)
        self.easyllm = EasyllmClient(self.api_key, self.project_id)


class ChatClient:
    def __init__(self, api_key, project_id):
        self.completions = Completions(api_key, project_id)


class AgentClient:
    def __init__(self, api_key, project_id):
        self.threads = Threads(api_key, project_id)


class EasyllmClient:
    def __init__(self, api_key, project_id):
        self.image_summarize = ImageSummarize(api_key, project_id)
        self.speech_to_text = SpeechToText(api_key, project_id)
        self.meeting_minutes = MeetingMinutes(api_key, project_id)
        self.pota_anlyst = PotaAnlyst(api_key, project_id)
        self.code_review = CodeReview(api_key, project_id)
        self.doc_summarizer = DocSummarizer(api_key, project_id)
        self.doc_parse = DocParse(api_key, project_id)


class ImageSummarize:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/image-summarizer'

    def create(self, easyllm_id: str, image_url: str, stream: bool = False) -> Union[
        Generator[ChatCompletionChunk, None, None], ChatCompletionResponse]:
        """
        在服务器上创建一个ImageSummarize，并可选择是否以流的形式接收响应。

        此方法向服务器发送数据，以便根据给定的 `easyllm_id` 和 `image_url` 创建一个新资源。
        如果指定，还可以处理流式响应。

        参数:
            easyllm_id (str): LLM实例的ID。
            image_url (str): 与请求相关联的图片URL。
            stream (bool, optional): 是否以流的形式接收响应，默认为False。

        返回:
            Any: 服务器的响应，可以是解析后的对象或原始流。

        异常:
            requests.HTTPError: 如果请求失败并返回HTTP错误。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'easyllm_id': easyllm_id,
            'image_url': image_url,
            'stream': stream
        }

        return get_chat_completion_response(self.base_url, data, headers, stream)


class SpeechToText:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/speechtotext/'

    def create(self, easyllm_id: str, audio_url: str) -> CreateTranscriptionResponse:
        """
        创建一个转录任务，并返回一个 CreateTranscriptionResponse 对象。

        参数:
            easyllm_id (str): LLM实例的ID。
            audio_url (str): 音频文件的URL。

        返回:
            CreateTranscriptionResponse: 包含任务ID和创建时间的响应对象。

        异常:
            requests.HTTPError: 如果请求失败并返回HTTP错误。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'easyllm_id': easyllm_id,
            'audio_url': audio_url,
        }
        try:
            response = requests.post(self.base_url + 'transcriptions', json=data, headers=headers)
            response.raise_for_status()  # 检查响应是否有错误
            return CreateTranscriptionResponse(response.json())
        except requests.RequestException as e:
            error_message = extract_error_message(response)
            raise RuntimeError(f"请求失败: {error_message}")

    def get(self, task_id: str) -> GetTranscriptionResponse:
        """
        根据任务ID获取转录任务的状态和结果。

        参数:
            task_id (str): 转录任务的ID。

        返回:
            GetTranscriptionResponse: 包含任务状态和转录结果的响应对象。

        异常:
            requests.HTTPError: 如果请求失败并返回HTTP错误。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(self.base_url + f'transcriptions/{task_id}', headers=headers)
            response.raise_for_status()
            return GetTranscriptionResponse(response.json())
        except requests.RequestException as e:
            error_message = extract_error_message(response)
            raise RuntimeError(f"请求失败: {error_message}")


class MeetingMinutes:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/meeting-minutes'

    def create(self, easyllm_id: str, meeting_transcript: str, stream: bool = False) -> Union[
        Generator[ChatCompletionChunk, None, None], ChatCompletionResponse]:
        """
                创建一个MeetingMinutes请求以发送数据到服务器。

                参数:
                easyllm_id (str): easyllmID,可从在服务列表处复制
                meeting_transcript (str): 会议的文字记录。
                stream (bool): 是否以流的形式处理响应，默认为False。

                返回:
                ChatCompletionResponse 或 流处理的结果，取决于stream参数。
                """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'easyllm_id': easyllm_id,
            'meeting_transcript': meeting_transcript,
            'stream': stream
        }
        return get_chat_completion_response(self.base_url, data, headers, stream)


class PotaAnlyst:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/pota-anlyst'

    def create(self, easyllm_id: str, prompt: str, stream: bool = False) -> Union[
        Generator[ChatCompletionChunk, None, None], ChatCompletionResponse]:
        """
                创建一个MeetingMinutes请求以发送数据到服务器。

                参数:
                easyllm_id (str): easyllmID,可从在服务列表处复制
                meeting_transcript (str): 会议的文字记录。
                stream (bool): 是否以流的形式处理响应，默认为False。

                返回:
                ChatCompletionResponse 或 流处理的结果，取决于stream参数。
                """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'easyllm_id': easyllm_id,
            'prompt': prompt,
            'stream': stream
        }
        return get_chat_completion_response(self.base_url, data, headers, stream)


class CodeReview:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/code-review'

    def create(self, easyllm_id: str, prompt: str, user_instruction: str = None, stream: bool = False) -> Union[
        Generator[ChatCompletionChunk, None, None], ChatCompletionResponse]:
        """
                创建一个MeetingMinutes请求以发送数据到服务器。

                参数:
                easyllm_id (str): easyllmID,可从在服务列表处复制
                prompt (str): diff文件内容
                user_instruction 用户自定义提示词
                stream (bool): 是否以流的形式处理响应，默认为False。

                返回:
                ChatCompletionResponse 或 流处理的结果，取决于stream参数。
                """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'easyllm_id': easyllm_id,
            'prompt': prompt,
            'user_instruction': user_instruction,
            'stream': stream
        }
        return get_chat_completion_response(self.base_url, data, headers, stream)


class DocSummarizer:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/doc-summarizer'

    def create(self, easyllm_id: str, prompt: str, stream: bool = False) -> Union[
        Generator[ChatCompletionChunk, None, None], ChatCompletionResponse]:
        """
                创建一个DocSummarizer请求以发送数据到服务器。

                参数:
                easyllm_id (str): easyllmID,可从在服务列表处复制
                prompt (str): 文档文本内容。
                stream (bool): 是否以流的形式处理响应，默认为False。

                返回:
                ChatCompletionResponse 或 流处理的结果，取决于stream参数。
                """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'easyllm_id': easyllm_id,
            'prompt': prompt,
            'stream': stream
        }
        return get_chat_completion_response(self.base_url, data, headers, stream)


class DocParse:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/easyllms/doc-parse'

    def create(self, easyllm_id: str, file_path: str) -> DocParseResponse:
        """
        文档内容解析。

        参数:
            easyllm_id (str): easyllmID,可从在服务列表处复制
            file_path (str): 文件路径

        返回:
            DocParseResponse: 包含解析结果的响应对象。

        异常:
            requests.HTTPError: 如果请求失败并返回HTTP错误。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }
        files = {
            'file': open(file_path, 'rb')
        }
        data = {
            'easyllm_id': easyllm_id,
        }
        try:
            response = requests.post(self.base_url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return DocParseResponse(response.json())
        except requests.RequestException as e:
            error_message = extract_error_message(response)
            raise RuntimeError(f"请求失败: {error_message}")


def extract_error_message(response):
    """从响应中提取错误信息"""
    try:
        error_response = response.json()
        error_message = error_response.get('message', '未知异常')
    except (ValueError, AttributeError):
        error_message = '未知异常'
    return error_message


class Completions:
    def __init__(self, api_key: str, project_id: str):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/chat/completions'

    def create(self, model_id: str, messages: List[Dict[str, Any]],
               frequency_penalty: Optional[float] = None, presence_penalty: Optional[float] = None,
               temperature: Optional[float] = None, max_tokens: Optional[int] = None,
               top_p: Optional[float] = None, stop: Optional[List[str]] = None,
               response_format: Optional[object] = None,
               stream: bool = False) -> Union[Generator[ChatCompletionChunk, None, None], ChatCompletionResponse]:
        """
        向服务器发送请求，创建一个新的聊天完成实例，并可选择是否以流的形式接收响应。

        此方法将模型ID和消息列表作为数据发送到服务器，根据这些信息创建聊天完成实例。
        如果指定，还可以以流的形式处理响应。

        参数:
            model_id (str): 使用的模型的ID。
            messages (List[Dict[str, Any]]): 聊天消息列表，每个消息为一个字典。
            frequency_penalty (float, optional): 频率惩罚参数，默认为None。
            presence_penalty (float, optional): 存在惩罚参数，默认为None。
            temperature (float, optional): 温度参数，默认为None。
            max_tokens (int, optional): 最大令牌数，默认为None。
            top_p (float, optional): 生成的概率质量函数的截断值，默认为None。
            stop (List[str], optional): 停止序列列表，默认为None。
            response_format (object,Optional):响应格式，默认为None。
            stream (bool, optional): 是否以流的形式接收响应，默认为False。

        返回:
            Any: 如果stream为True，返回从服务器流式传输的数据；如果为False，则返回解析后的聊天完成响应。

        异常:
            requests.HTTPError: 如果请求失败并返回HTTP错误。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model_id': model_id,
            'messages': messages,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'stop': stop,
            'response_format': response_format,
            'stream': stream
        }

        return get_chat_completion_response(self.base_url, data, headers, stream)


class Threads:
    def __init__(self, api_key: str, project_id: str):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'https://platform.fastmodels.cn/api/open-apis/projects/{project_id}/agents/runs'

    def create_and_run(self, agent_id: str, messages: List[Dict[str, Any]], thread_id: str = None, stream: bool = False) -> Union[
        Generator[AgentCompletionChunk, None, None], AgentCompletionResponse]:
        """
        向服务器发送请求，创建一个新的聊天完成实例，并可选择是否以流的形式接收响应。

        此方法将agent_id和消息列表作为数据发送到服务器，根据这些信息创建聊天完成实例。

        参数:
            agent_id (str): 使用的agent的ID。
            messages (List[Dict[str, Any]]): 聊天消息列表，每个消息为一个字典，包括角色和内容（支持的内容类型请参照API列表）
            stream (bool, optional): 是否以流的形式接收响应，默认为False。

        返回:
            Any: 如果stream为True，返回从服务器流式传输的数据；如果为False，则返回解析后的聊天完成响应。

        异常:
            requests.HTTPError: 如果请求失败并返回HTTP错误。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "thread": {
                "thread_id": thread_id,
                "messages": messages
            },
            "agent_id": agent_id,
            "stream": stream
        }

        return get_agent_completion_response(self.base_url, data, headers, stream)


def get_chat_completion_response(base_url, data, headers, stream):
    """发送请求并处理响应"""
    try:
        response = requests.post(base_url, json=data, headers=headers, stream=stream)
        response.raise_for_status()  # 检查响应是否有错误

        if stream:
            return parse_chat_stream(response.iter_lines())
        else:
            return ChatCompletionResponse(response.json())
    except requests.RequestException:
        error_message = extract_error_message(response)
        raise RuntimeError(f"请求失败: {error_message}")


def get_agent_completion_response(base_url, data, headers, stream):
    """发送请求并处理响应"""
    try:
        response = requests.post(base_url, json=data, headers=headers, stream=stream)
        response.raise_for_status()  # 检查响应是否有错误
        if stream:
            return parse_agent_stream(response.iter_lines())
        else:
            return AgentCompletionResponse(response.json())

    except requests.RequestException:
        error_message = extract_error_message(response)
        raise RuntimeError(f"请求失败: {error_message}")
