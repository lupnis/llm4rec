import argparse
from fastapi import FastAPI
import uvicorn
from pathlib import Path
from typing import (Any, Callable, List, Optional)
import datetime

import json

userdb = {}
with open('./user_db.json', 'r', encoding='utf-8') as f:
    userdb = json.loads(f.read())
    
def verify_login(uname, hashpwd):
    return userdb.get(uname) and userdb[uname]["password"] == hashpwd

def get_user_info(uname):
    dret =  userdb.get(uname, {"user_id": "undefined",
        "user_name": "no account",
        "password": "no password",
        "saved_pref": []})
    dret["password"] = ''
    return dret


from langchain.schema import (BaseMessage, AIMessage, HumanMessage)
BaseMessage()

class SessionManager:
    def __init__(self, store_session: bool = False, load_session: bool = False, session_store_path: Optional[Path] = None):
        self.sessions = {}
        self.session_infos = {}

    def session_exists(self, session_id: str):
        return self.session_infos.get(session_id) and self.sessions.get(session_id)

    def create_session(self, session_id: str, overwrite_exist: bool = True, init_data: Optional[List[BaseMessage]] = None):
        if self.session_exists(session_id) and not overwrite_exist:
            return False
        self.session_infos[session_id] = {
            "session_id": session_id,
            "create_at": datetime.datetime.now(),
            "turns": 0,
            "terminated": False
        }
        self.sessions[session_id] = [] if not init_data else init_data
        return True

    def stop_session(self, session_id: str, keep_session_data: bool = False):
        if not self.session_exists(session_id):
            return False
        self.session_infos[session_id]["terminated"] = True
        if not keep_session_data:
            del self.session_infos[session_id]
            del self.sessions[session_id]
        return True

    def add_data(self, session_id: str, data: Optional[List[BaseMessage]] = None):
        if not self.session_exists(session_id) or not data:
            return False
        self.session_infos[session_id]["turns"] += 1
        self.sessions[session_id] += data
        return True

    def get_data(self, session_id: str):
        return self.sessions.get(session_id, [])

    def get_session_status(self, session_id: str):
        return self.session_infos.get(session_id)


class ChatManager:
    def __init__(self, model_path: str, checkpoint_path: str, max_turns: int = 30):
        ...


def stdmsg(status: int = 200, message: str = "", data: Any = None):
    return {
        "status": status,
        "message": message,
        "data": data
    }






def App(session_manager: SessionManager, parent: FastAPI = None, auth_fn: Callable = None):
    if not parent:
        parent = FastAPI()

    @parent.get('/')
    async def root_path_controller():
        return stdmsg(message="hello llm4rec")

    @parent.post('/session/create/{auth}/{init_prefs}')
    async def session_create_controller(auth, init_prefs):
        if not auth_fn or (auth_fn and auth_fn(auth)):
            ...  # todo: generate session code, create session data storage
            # todo: init chat data with initial user preferences
            session_manager.create_session(
                "test1", init_data=[{"role": "user", "content": f"the user has the following preferences:{init_prefs}"}])
            return stdmsg(message="authorization succeeded", data={"session_id": 1, "more": session_manager.get_data("test1"), "more2": session_manager.get_session_status("test1")})
        else:
            return stdmsg(400, "authorization failed")

    @parent.post('/session/chat/{session_id}/{prompt}')
    async def session_chat_controller(session_id, prompt):
        return stdmsg()

    @parent.post('/session/stop/{session_id}')
    async def session_end_controller(session_id):
        return stdmsg()

    @parent.get('/session/status/{session_id}')
    async def session_status_controller(session_id):
        return stdmsg()
    
    
    @parent.post('/login')
    async def user_login(username, pwdhash):
        if verify_login(user_login, pwdhash):
            return stdmsg(message='succeeded')
        else:
            return stdmsg(-1, 'failed')
    

    return parent


def parse_args():
    parser = argparse.ArgumentParser(
        "ChatAPI Pack", None, "LLM4REC Backend AI SEARCH PART")
    parser.add_argument("--model", type=str, default="THUDM/chatglm3-6b",
                        help="recommendation base llm model path")
    parser.add_argument("--max-turns", type=int, default=30,
                        help="max turns of a session")
    return parser.parse_args()


app = App(SessionManager())
if __name__ == "__main__":
    opt = parse_args()
    # print(opt)

    uvicorn.run(app)
