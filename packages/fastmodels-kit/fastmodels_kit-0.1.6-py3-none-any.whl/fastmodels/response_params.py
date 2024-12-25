import json
from typing import Dict, Any, Generator, Iterable, Optional, List


class CreateTranscriptionResponse:
    """
        表示创建转录任务的响应数据的类。

        此类封装了从转录服务返回的响应数据，并提供了便捷的方式来访问任务ID和创建时间。

        Attributes:
            task_id (str): 转录任务的唯一标识符。如果响应中没有包含任务ID，则为None。
            created (long): 转录任务的创建时间。
        """

    def __init__(self, response_data: Dict[str, Any]):
        """
                使用从转录服务返回的响应数据初始化 CreateTranscriptionResponse 对象。

                Args:
                    response_data (Dict[str, Any]): 包含转录任务详细信息的字典，通常包括任务ID和创建时间。
                """
        self.task_id = response_data.get('task_id')
        self.created = response_data.get('created')


class GetTranscriptionResponse:
    """
        表示获取转录任务状态的响应数据的类。

        此类封装了从转录服务返回的响应数据，并提供了便捷的方式来访问任务ID、状态和结果。

        Attributes:
            task_id (str): 转录任务的唯一标识符
            status (str): 转录任务的当前状态
            result (str): 转录任务的结果
            audio_duration (float): 音频时长
        """

    def __init__(self, response_data: Dict[str, Any]):
        """
                使用从转录服务返回的响应数据初始化 GetTranscriptionResponse 对象。

                Args:
                    response_data (Dict[str, Any]): 包含转录任务详细信息的字典。
                """
        self.task_id = response_data.get('task_id')
        self.status = response_data.get('status')
        self.result = response_data.get('result')
        self.audio_duration = response_data.get('audio_duration')

class DocParseResponse:
    """
        表示文档解析助手的响应体。

        Attributes:
            data (str): 解析结果

        """

    def __init__(self, response_data: Dict[str, Any]):
        """
                使用从转录服务返回的响应数据初始化 GetTranscriptionResponse 对象。

                Args:
                    response_data (Dict[str, Any]): 包含转录任务详细信息的字典。
                """
        self.data = response_data.get('data')


class FileCitation:
    def __init__(self, quote: Optional[str], file_id: str, filename: str):
        self.quote = quote
        self.file_id = file_id
        self.filename = filename

class Annotation:
    def __init__(self, text: str, type: str, start_index: int, end_index: int, file_citation: Dict[str, Any]):
        self.text = text
        self.type = type
        self.start_index = start_index
        self.end_index = end_index
        self.file_citation = FileCitation(**file_citation)

class Text:
    def __init__(self, value: str, annotations: List[Dict[str, Any]] = None):
        self.value = value
        if annotations is None:
            self.annotations = []
        else:
            self.annotations = [Annotation(**annotation) for annotation in annotations]

class ContentItem:
    def __init__(self, type: str, text: Dict[str, Any]):
        self.type = type
        self.text = Text(**text)
class AgentCompletionResponse:
    """
       表示模型完成AgentCompletion任务的响应数据的类。

       此类封装了从AgentCompletion服务返回的响应数据，并提供了便捷的方式来访问相关属性和选择列表。

       Attributes:
           object (str): 响应对象的类型

       """

    def __init__(self, response_data: Dict[str, Any]):
        self.object = response_data.get('object')
        self.content = [ContentItem(**item) for item in response_data.get('content', [])]
        self.finish_reason = response_data.get('finish_reason')
        self.thread_id = response_data.get('thread_id')


class ChatCompletionResponse:
    """
       表示模型完成ChatCompletion任务的响应数据的类。

       此类封装了从ChatCompletion服务返回的响应数据，并提供了便捷的方式来访问相关属性和选择列表。

       Attributes:
           object (str): 响应对象的类型
           created (long): 创建时间。
           model (str): 使用的模型标识。
           choices (List[ChatChoice]): 聊天模型生成的选择列表，每个选择封装在 `ChatChoice` 类中。
       """

    def __init__(self, response_data: Dict[str, Any]):
        """
                使用从聊天模型服务返回的响应数据初始化 ChatCompletionResponse 对象。

                Args:
                    response_data (Dict[str, Any]): 包含聊天完成任务详细信息的字典。
                """
        self.object = response_data.get('object')
        self.created = response_data.get('created')
        self.model = response_data.get('model')
        self.choices = [ChatChoice(choice) for choice in response_data.get('choices', [])]


class ChatChoice:
    """
        表示非流式聊天生成的单个选择的类。

        此类封装了一个选择的详细信息，包括索引、消息和完成原因。

        Attributes:
            index (int): 选择的索引。
            message (ChatMessage): 与此选择相关的消息对象。
            finish_reason (Optional[str]): 完成此选择的原因，如果响应中没有包含完成原因，则为None。
        """

    def __init__(self, choice_data: Dict[str, Any]):
        """
                使用从聊天模型服务返回的选择数据初始化 ChatChoice 对象。

                Args:
                    choice_data (Dict[str, Any]): 包含选择详细信息的字典。
                """
        self.index = choice_data.get('index')
        self.message = ChatMessage(choice_data['message'])
        self.finish_reason = choice_data.get('finish_reason')


class ChatMessage:
    """
       表示聊天消息的类。

       此类封装了聊天消息的详细信息，包括消息内容和角色。

       Attributes:
           content (Optional[str]): 消息的文本内容，如果响应中没有包含内容，则为None。
           role (Optional[str]): 发送消息的角色（如用户、系统等），如果响应中没有包含角色，则为None。
       """

    def __init__(self, message_data: Dict[str, Any]):
        """
        使用从聊天模型服务返回的消息数据初始化 ChatMessage 对象。

        Args:
            message_data (Dict[str, Optional[str]]): 包含消息详细信息的字典。
        """
        self.content = message_data.get('content')
        self.role = message_data.get('role')


class ChatCompletionChunk:
    def __init__(self, chunk_data: Dict[str, Any]):
        """
        初始化一个聊天完成块实例。

        参数:
        chunk_data (Dict[str, Any]): 包含聊天块数据的字典。

        属性:
        object (str): 对象类型。
        created (int): 创建时间戳。
        model (str): 使用的模型。
        choices (List[ChatChunkChoice]): 包含选择的列表。
        """
        self.object = chunk_data.get('object')
        self.created = chunk_data.get('created')
        self.model = chunk_data.get('model')
        self.choices = [ChatChunkChoice(choice) for choice in chunk_data.get('choices', [])]


class AgentCompletionChunk:
    def __init__(self, chunk_data: Dict[str, Any]):
        """
        初始化一个消息变动块实例。

        参数:
        chunk_data (Dict[str, Any]): 包含消息变动数据的字典。

        属性:
        object (str): 对象类型。
        delta (MessageDelta): 消息内容的变动。
        thread_id (str): 线程ID。
        finish_reason (Optional[str]): 完成原因，可能为None。
        """
        self.object = chunk_data.get('object')
        self.thread_id = chunk_data.get('thread_id')
        delta_data = chunk_data.get('delta')
        self.delta = AgentMessageDelta(delta_data) if delta_data is not None else None
        self.finish_reason = chunk_data.get('finish_reason', None)


class ChatMessageDelta:
    """
    表示聊天消息变化的类。

    此类封装了聊天消息的变化细节，如内容和角色。

    Attributes:
        content (Optional[str]): 消息变化的文本内容，如果响应中没有包含内容，则为None。
        role (Optional[str]): 发送消息变化的角色（如用户、系统等），如果响应中没有包含角色，则为None。
    """

    def __init__(self, delta_data: Dict[str, Any]):
        """
        使用从聊天模型服务返回的消息变化数据初始化 ChatMessageDelta 对象。

        Args:
            delta_data (Dict[str, Optional[str]]): 包含消息变化详细信息的字典。
        """
        self.content = delta_data.get('content')
        self.role = delta_data.get('role')


class TextAnnotation:
    def __init__(self, annotations_data: Optional[List[Dict[str, Any]]]):
        # 根据annotations的数据结构初始化，可以为空或列表
        self.annotations = annotations_data if annotations_data is not None else []


class TextContent:
    def __init__(self, content_data: Dict[str, Any]):
        self.type = content_data.get('type')
        self.value = content_data['text']['value']
        # 处理annotations，可能是None
        self.annotations = TextAnnotation(content_data['text'].get('annotations'))


class AgentMessageDelta:
    def __init__(self, delta_data: Dict[str, Any]):
        # 解析 delta 数据中的 content 部分，使用列表推导式和之前定义的 ContentItem
        self.content = [ContentItem(**item) for item in delta_data.get('content', [])]

    def to_dict(self):
        # 将对象转换回字典形式，主要用于输出或调试
        return {
            'content': [self.content_item_to_dict(item) for item in self.content]
        }


class ChatChunkChoice:
    """
    表示聊天模型生成的一个分块选择的类。

    此类封装了一个选择的详细信息，包括索引、消息变化和完成原因。

    Attributes:
        index (Optional[int]): 选择的索引，如果响应中没有包含索引，则为None。
        delta (ChatMessageDelta): 与此选择相关的消息变化对象。
        finish_reason (Optional[str]): 完成此选择的原因，如果响应中没有包含完成原因，则为None。
    """

    def __init__(self, choice_data: Dict[str, Any]):
        """
        使用从聊天模型服务返回的选择数据初始化 ChatChunkChoice 对象。

        Args:
            choice_data (Dict[str, Any]): 包含选择详细信息的字典。
        """
        self.index = choice_data.get('index')
        self.delta = ChatMessageDelta(choice_data.get('delta', {}))
        self.finish_reason = choice_data.get('finish_reason')


def parse_chat_stream(lines: Iterable[bytes]) -> Generator['ChatCompletionChunk', None, None]:
    """
    解析流式响应中的行，生成聊天完成块。

    参数:
        lines (Iterable[bytes]): 从服务器接收到的原始字节行。

    返回:
        Generator[ChatCompletionChunk, None, None]: 生成聊天完成块的生成器。
    """
    for line in lines:
        if line.strip():
            yield ChatCompletionChunk(json.loads(line.decode('utf-8').replace('data:', '').strip()))


def parse_agent_stream(lines: Iterable[bytes]) -> Generator['AgentCompletionChunk', None, None]:
    """
    解析流式响应中的行，生成聊天完成块。

    参数:
        lines (Iterable[bytes]): 从服务器接收到的原始字节行。

    返回:
        Generator[ChatCompletionChunk, None, None]: 生成聊天完成块的生成器。
    """
    for line in lines:
        if line.strip():
            yield AgentCompletionChunk(json.loads(line.decode('utf-8').replace('data:', '').strip()))
