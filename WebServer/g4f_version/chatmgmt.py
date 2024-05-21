from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
import datetime
import os

from g4f.client import Client

os.environ["HF_ENDPOINT"] = 'https://hf-mirror.com'
proxies = {
    "all": "http://127.0.0.1:7890"
}

class ChatManager:
    def __init__(self, store_session=False, load_session=False, session_store_path=None):
        self.llm = Client(proxies=proxies)
        self.sessions = {}

    def session_exists(self, session_id: str):
        return self.sessions.get(session_id)

    def create_session(self, session_id: str, max_turns=50, overwrite_exist: bool = True):
        if self.session_exists(session_id) and not overwrite_exist:
            return False
        self.sessions[session_id] = {
            "session_id": session_id,
            "create_at": datetime.datetime.now(),
            "max_turns": max_turns,
            "memory": [],
            "terminated": False
        }
        self.sessions[session_id]["memory"].append({"role":"system","content":"data of preferences and game recommendations provided are SUMMARIZED FORM THE CURRENT USER."})
        return True

    def stop_session(self, session_id: str, keep_session_data: bool = False):
        if not self.session_exists(session_id):
            return False
        self.sessions[session_id]["terminated"] = True
        if not keep_session_data:
            del self.sessions[session_id]
        return True

    def chat(self, session_id, content=None):
        if not content or content == "" or not self.session_exists(session_id):
            return {"status": 0, "reason": "invalid query"}
        if len(self.sessions[session_id]["memory"]) >= self.sessions[session_id]["max_turns"]:
            return {"status": 0, "reason": "max turns exceeded"}
        self.sessions[session_id]["memory"].append({"role":"user","content":content})
        comp = self.llm.chat.completions.create(model="gpt-3.5-turbo",messages=self.sessions[session_id]["memory"])
        answer = comp.choices[0].message.content or ""
        self.sessions[session_id]["memory"].append({"role":"assistant","content":answer})
        return {"status": 200, "answer": answer}

    def get_data(self, session_id: str):
        if not self.session_exists(session_id):
            return []
        return [msg["content"] for msg in self.sessions[session_id]["memory"]]

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
