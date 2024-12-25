import json
from docarray import BaseDoc, DocList
from typing import Dict, Optional, Literal, List
import srsly
from pydantic import Field, validate_arguments

class ToolParam(BaseDoc):
    """定义工具的一个参数"""
    name: str = Field(description="参数名称")
    type: str = Field(description="符合JSON Scheme规范的参数类型，如string, boolean, integer, number")
    description: str = Field(description="参数描述")
    enum: List[str, int, float] = Field(default_factory=list, description="参数可选值列表，限定参数值只能从其中选择")
    required: bool = Field(description="参数是否必填")

    def to_openai_format(self) -> Dict:
        """
        :return: (name, properties dict)
        """
        schema = {
            'type': self.type,
            'description': self.description,
        }
        if self.enum:
            schema['enum'] = self.enum
        return schema


class Tool(BaseDoc):
    """定义一个工具"""
    name: str = Field(description="工具名称")
    description: str = Field(description="工具描述")
    parameters: List[ToolParam] = Field(description="工具参数，key为参数名，value为参数描述")

    def to_openai_format(self) -> Dict:
        properties = dict()
        required = []
        for param in self.parameters:
            properties[param.name] = param.to_openai_format()
            if param.required:
                required.append(param.name)

        schema = {
                'type': 'function',
                'function': {
                'name': self.name,
                'description': self.description,
                'parameters': {
                    'type': 'object',
                    'properties': properties
                }
            }
        }
        if required:
            schema['function']['parameters']['required'] = required
        return schema


class Message(BaseDoc):
    role: Literal['user', 'assistant', 'system', 'developer', 'tool'] = Field(description="message角色, 必须是['user', 'assistant', 'system', 'developer', 'tool']中的一个")
    content: str = Field(description="message内容", default=None)


class ToolCallParam(BaseDoc):
    name: str = Field(description="工具调用名称")
    arguments: str = Field(description="工具调用参数，JSON样式字符串")


class ToolCallMessageParam(BaseDoc):
    id: str = Field(description="工具调用id")
    type: Literal['function'] = Field(default='function', description="工具类型，必须为['function']")
    function: ToolCallParam = Field(description="工具调用内容")

    def to_openai_format(self):
        return {
            'id': self.id,
            'type': self.type,
            'function': {
                'name': self.function.name,
                'arguments': self.function.arguments
            }
        }


class ToolCallMessage(Message):
    role: Literal['assistant'] = Field(default='assistant', description="message角色, 必须是['assistant']")
    tool_calls: List[ToolCallMessageParam] = Field(description="由模型生成的工具调用列表")

    def to_openai_format(self):
        return {
            'role': self.role,
            'content': self.content,
            'tool_calls': [tool_call.to_openai_format() for tool_call in self.tool_calls]
        }


class MessageFromTemplate(Message):
    """通过模版和参数来format content，主要可以确保修改message模版后的旧数据依然可用
    """
    template: str = Field(description="message模版，其中的参数通过kwargs来填充，便于修改模板后重新构建message", default=None)
    kwargs: Dict[str, str] = Field(description="message 参数，便于修改模板后重新构建message", default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.template is not None and self.kwargs is not None:
            self.content = self.template.format(**self.kwargs)
        else:
            raise ValueError("必须提供template和kwargs")
        
    
class DialogueDoc(BaseDoc):
    """存放openai格式的对话历史
    """
    system: Optional[str] = None
    system_message: Message = None
    tools: Optional[List[Tool]] = None
    conversation: DocList[Message] = Field(default_factory=DocList[Message])
    theme: Optional[str] = None
    situation: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.system is not None and self.system_message is None:
            self.system_message = Message(role="system", content=self.system)
        
    @property
    def messages(self):
        list = []
        # 兼容旧数据中system
        if self.system is not None and self.system_message is None:
            self.system_message = Message(role="system", content=self.system)
        if self.system_message is not None:
            list.append(self.system_message)
        list.extend(self.conversation)
        return list
    
    
    
class DialogueDocList(DocList[DialogueDoc]):
    
    @classmethod
    def from_instruction_json(cls, json_path: str) -> "DialogueDocList":
        """json格式需要为instruction, input, output, history
        注意:
        - history的格式应为[$input, $output].
        - role只能为user或者assistant.
        """
        docs = DialogueDocList()
        for line in srsly.read_json(json_path):
            doc = DialogueDoc(system=line['system'])
            if line['history']:
                for i, his in enumerate(line['history']):
                    if i % 2 == 0:
                        doc.conversation.append(Message(role="user", content=his))
                    else:
                        doc.conversation.append(Message(role="assistant", content=his))
                        
            input_message = Message(role='user', content=line['input'])
            output_message = Message(role='assistant', content=str(line['output']))
            doc.conversation.append(input_message)
            doc.conversation.append(output_message)
            docs.append(doc)
        return docs
    
    def to_instruction_json(self, json_path, **dump_kwargs) -> None:
        """转换为instruction json数据格式

        Args:
            jsonl_path (str): 保存的jsonl文件
        """
        json_data = []
        for d in self:
            input_message = d.conversation[-2]
            output_message = d.conversation[-1]
            line = {"system": d.system}
            
            if len(d.conversation) <= 2:
                line['history'] = []
            else:
                i = 0
                while i+1 < len(d.conversation[:-2]):
                    line['history'].append(d.conversation[i].content, d.conversation[i+1].content)
                    i += 2
            line['output'] = output_message.content
            line['instruction'] = input_message.content
            json_data.append(line)
        
        json.dump(json_data, open("json_path", "w", encoding="utf-8"),**dump_kwargs)
        
        
    
    @classmethod
    def from_qwen_jsonl(cls, jsonl_path:str) -> "DialogueDocList":
        """从千问的jsonl数据格式导入doc

        Args:
            jsonl_path (str): qwen jsonl文件
        """
        docs = DialogueDocList()
        for line in srsly.read_jsonl(jsonl_path):
            source = line['source']
            doc = DialogueDoc(id=source)
            doc.tags.append(source.split("-")[1])
            for m in line['messages']:
                if m['role'] == 'system':
                    doc.system = m['content']
                else:
                    doc.conversation.append(Message(role=m['role'], content=m['content']))
            docs.append(doc)
        return docs
    
    def to_qwen_jsonl(self, jsonl_path:str, **dump_kwargs) -> None:
        """转换为千问的jsonl数据格式

        Args:
            jsonl_path (str): 保存的jsonl文件
            dump_kwargs: json dump参数
        """
        with open(jsonl_path, "w", encoding="utf-8") as fo:
            for d in self:
                line = {"type": "chatml", "source": d.id, "messages":[]}
                messages = d.messages
                line['messages'] = [{"role":m.role, "content":m.content} for m in messages]
                fo.write(json.dumps(line, **dump_kwargs)+"\n")
    
    def to_openai_format_json(self, json_path:str, **dump_kwargs) -> None:
        """转换为openai的数据格式：
            [
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "system prompt (optional)"
                        },
                        {
                            "role": "user",
                            "content": "human instruction"
                        },
                        {
                            "role": "assistant",
                            "content": "model response"
                        }
                    ]
                }
            ]<br>
            如果需要在llama-factory中使用，需要按下列格式配置dataset_info.json(https://github.com/hiyouga/LLaMA-Factory)
            {
                "openai_fmt_train": { ---> 数据名称
                    "file_name": "openai_fmt_train.json",   ---> 数据文件路径（相对于data目录的相对路径）
                    "formatting": "sharegpt",
                    "columns": {
                        "messages": "messages"
                    },
                    "tags": {
                        "role_tag": "role",
                        "content_tag": "content",
                        "user_tag": "user",
                        "assistant_tag": "assistant",
                        "system_tag": "system"
                    }
            }
        Args:
            json_path (str): 保存的json文件
            dump_kwargs: json dump参数
        """
        json_data = []
        for d in self:
            line = {"messages":[]}
            for m in d.messages:
                if isinstance(m, ToolCallMessage):
                    message = m.to_openai_format()
                else:
                    message = {"role": m.role, "content": m.content}
                line['messages'].append(message)
            json_data.append(line)
        json.dump(json_data, open(json_path, "w", encoding="utf-8"), **dump_kwargs)

    @validate_arguments
    def quick_add(self, conversation: List[str], system: str = None, theme: str = None, situation: str = None):
        """快速添加对话,默认user在前,assistant在后,且交替出现
        """
        doc = DialogueDoc(system=system, theme=theme, situation=situation)
        for i, message in enumerate(conversation):
            if i % 2 == 0:
                doc.conversation.append(Message(role='user', content=message))
            else:
                doc.conversation.append(Message(role='assistant', content=message))
        self.append(doc)
