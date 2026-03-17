import os,json
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage

#message_to_dict:单个消息对象，BaseMessage->字典，单个转单个
#messages_from_dict:[字典、字典…]->[消息、消息...]
#AIMessage HumanMessage SystemMessage都是BaseMessage子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id=session_id
        self.storage_path=storage_path
        self.file_path=os.path.join(self.storage_path,self.session_id)
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)
    def add_messages(self,messages:Sequence[BaseMessage])->None:
        all_messages=list(self.messages)
        all_messages.extend(messages)#新老融合成一个list
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([message_to_dict(message) for message in all_messages],f)
            # 将list转成json
    @property
    def messages(self)->list[BaseMessage]:
        #当前文件内：list[字典]
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                messages=json.load(f)
                return messages_from_dict(messages)
        except FileNotFoundError:
            return []

    def clear(self):
        self.messages=[]
        with open(self.file_path,"w") as f:
            json.dump([],f)#直接写入空列表