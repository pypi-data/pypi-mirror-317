from nlp_data.utils import check_pydantic_version
from ..document import DialogueDoc, DialogueDocList, FucntionCallDialogueDoc, FucntionCallDialogueDocList
from .base import BaseDocStore
from docarray import DocList


class DialogueDocStore(BaseDocStore):
    
    bucket_name = 'dialogue'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> DialogueDocList:
        name = name.strip()
        docs = DocList[DialogueDoc].pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
        return DialogueDocList(docs)
    
    @classmethod
    @check_pydantic_version()
    def push(cls, docs: DocList[DialogueDoc], name: str, show_progress: bool = True) -> None:
        name = name.strip()
        _ = DocList[DialogueDoc].push(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
        return None
    
class FunctionCallDialogueDocStore(BaseDocStore):
    
    bucket_name = 'function_call'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> DocList[FucntionCallDialogueDoc]:
        name = name.strip()
        docs = DocList[FucntionCallDialogueDoc].pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
        return FucntionCallDialogueDocList(docs)
    
    @classmethod
    def push(cls, docs: DocList[FucntionCallDialogueDoc], name: str, show_progress: bool = True) -> None:
        name = name.strip()
        _ = DocList[FucntionCallDialogueDoc].push(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
        return None    