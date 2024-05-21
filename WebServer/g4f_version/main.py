import fastapi
from fastapi import Query
import datetime
import json
import hashlib
import time

from chatmgmt import PlainTextLoader, ChatManager
from gamemgmt import GameManager
from usermgmt import UserManager


def stdmsg(status: int = 200, message: str = "", data=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }



user_manager = UserManager('./data/user_db.json')
game_manager = GameManager('./data/game_db.json',
                           './data/inverted_index_db.json')



chat_manager = ChatManager()
crypter = hashlib.md5()


def App():
    global user_manager, game_manager, chat_manager, crypter
    app = fastapi.FastAPI()

    @app.post('/api/user/login')
    async def login(username, hashedpwd):
        ret = user_manager.login(username, hashedpwd)
        return stdmsg(200 if ret else 0, "succeeded" if ret else "failed", ret)

    @app.post('/api/user/vlogin')
    async def verify_login(uname, sessionid):
        ret = user_manager.verify_login(uname, sessionid)
        return stdmsg(200 if ret else 0, "ok" if ret else "invalid")

    @app.post('/api/user/logout')
    async def logout(uname, sessionid):
        ret = user_manager.logout(uname, sessionid)
        return stdmsg(200 if ret else 0, "succeeded" if ret else "failed")

    @app.get('/api/user/info')
    async def get_account_info(uname, sessionid):
        ret = user_manager.get_user_info(uname, sessionid)
        return stdmsg(200 if ret else 0, "succeeded" if ret else "failed", ret)

    @app.post('/api/game/search')
    async def search_game(game_name=None, top_k: int = 10, tag_filter: list = Query(None), price_range: list = Query(None)):
        return stdmsg(200, "ok", game_manager.search_game(game_name, tag_filter, price_range, top_k))

    @app.post('/api/game/recommend')
    async def recommend_game(uname=None, sessionid=None, top_k: int = 10):
        if not uname or not sessionid:
            return stdmsg(0, "no account info")
        user_prefs = user_manager.get_user_info(uname, sessionid)["saved_pref"]
        game_candidates = game_manager.search_game('', user_prefs[0] if user_prefs else None, [
                                                   0, user_prefs[1]] if user_prefs else None, top_k)
        return stdmsg(200, "ok", game_candidates)

    # ######################################
    # chat parts
    @app.post('/api/chat/create')
    async def create_session(uname, sessionid):
        if not user_manager.verify_login(uname, sessionid):
            return stdmsg(0, "auth failed")
        crypter.update(str.encode(
            f'{time.time()}{uname}{sessionid}', encoding='utf-8'))
        chat_session_id = crypter.hexdigest()

        user_prefs = user_manager.get_user_info(uname, sessionid)["saved_pref"]
        game_candidates = game_manager.search_game('', user_prefs[0] if user_prefs else None, [
                                                   0, user_prefs[1]] if user_prefs else None)
        documents = [
           {"role":"system", "content": f"The user prefers following types of games: {user_prefs[0]}."},
           {"role":"system", "content": f"The user can accept games of price no more than ${user_prefs[1]}."},
           {"role":"system", "content": f"Recommendation details of games the user might want to play in JSON format: {game_candidates}."},
           {"role":"system", "content": f"Ignore all hyperlinks to urls"},
           {"role":"system", "content":"do not return game recommendations or game details when not asked for recommendations"}
        ]
        res = chat_manager.create_session(chat_session_id)
        for item in documents:
            chat_manager.sessions[chat_session_id]["memory"].append(item)
        return stdmsg(200 if res else 0, 'ok' if res else 'failed', chat_session_id)

    @app.post('/api/chat/stop')
    async def stop_session(uname, sessionid, chat_sessionid):
        if not user_manager.verify_login(uname, sessionid):
            return stdmsg(0, "auth failed")
        ret = chat_manager.stop_session(chat_sessionid)
        return stdmsg(200 if ret else 0, 'succeeded' if ret else 'failed')

    @app.post('/api/chat/verify')
    async def verify_session(uname, sessionid, chat_sessionid):
        if not user_manager.verify_login(uname, sessionid):
            return stdmsg(0, "auth failed")
        ret = chat_manager.session_exists(chat_sessionid)
        return stdmsg(200 if ret else 0, 'ok' if ret else 'invalid')

    @app.post('/api/chat/chat')
    async def send_chat(chat_sessionid, content=None):
        if not chat_manager.session_exists(chat_sessionid):
            return stdmsg(0, "session invalid")
        ret = chat_manager.chat(chat_sessionid, content)
        return ret

    @app.get('/api/chat/history')
    async def get_history(chat_sessionid):
        if not chat_manager.session_exists(chat_sessionid):
            return stdmsg(0, "session invalid")
        return chat_manager.get_data(chat_sessionid)

    return app


app = App()
