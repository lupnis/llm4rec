from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
import datetime
import os
import copy
from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    BaseMessage,
    HumanMessage,
    get_buffer_string,
)

os.environ["HF_ENDPOINT"] = 'https://hf-mirror.com'


class ChatManager:
    def __init__(self, llm, embeddings, store_session=False, load_session=False, session_store_path=None):
        self.llm = llm
        self.embeddings = embeddings
        self.sessions = {}

    def session_exists(self, session_id: str):
        return self.sessions.get(session_id)

    def create_session(self, session_id: str, vectorstore, max_turns=20, overwrite_exist: bool = True):
        if self.session_exists(session_id) and not overwrite_exist:
            return False
        self.sessions[session_id] = {
            "session_id": session_id,
            "create_at": datetime.datetime.now(),
            "max_turns": max_turns,
            "retriever": vectorstore.as_retriever(),
            "memory": ConversationBufferMemory(llm=self.llm, memory_key="chat_history", return_messages=True),
            "terminated": False
        }
        self.sessions[session_id]["memory"].chat_memory.add_message(SystemMessage(content='data of preferences and game recommendations provided are ALL SUMMARIZED FORM THE CURRENT USER.'))
        self.sessions[session_id]["qa"] = ConversationalRetrievalChain.from_llm(
            self.llm, retriever=self.sessions[session_id]["retriever"], memory=self.sessions[session_id]["memory"])
        return True

    def stop_session(self, session_id: str, keep_session_data: bool = False):
        if not self.session_exists(session_id):
            return False
        self.sessions[session_id]["terminated"] = True
        if not keep_session_data:
            del self.sessions[session_id]
        return True

    def chat(self, session_id, context=None):
        if not context or context == "" or not self.session_exists(session_id):
            return {"status": 0, "reason": "invalid query"}
        if len(self.sessions[session_id]["memory"].chat_memory.messages) >= self.sessions[session_id]["max_turns"]:
            return {"status": 0, "reason": "max turns exceeded"}
        return {"status": 200, "answer": self.sessions[session_id]["qa"].invoke(context)["answer"]}

    def get_data(self, session_id: str):
        if not self.session_exists(session_id):
            return []
        return [msg.content for msg in self.sessions[session_id]["memory"].chat_memory.messages]

    def get_session_status(self, session_id: str):
        session = self.sessions.get(session_id)
        if not session:
            return {"status": 0, "reason": "invalid query"}
        else:
            return {
                "status": 200,
                "session_id": session["session_id"],
                "create_at": session["create_at"],
                "max_turns": session["max_turns"],
                "memory": self.get_data(session_id)
            }


class PlainTextLoader(BaseLoader):
    def __init__(self, texts: str):
        self.texts = texts

    def lazy_load(self):
        yield from [
            Document(page_content=tt, metadata={
                     "source": "plain text", "page": i})
            for i, tt in enumerate(self.texts)]
