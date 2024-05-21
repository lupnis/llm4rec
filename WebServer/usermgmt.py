import json
import hashlib
import time
import copy


class UserManager:
    def __init__(self, db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            self.db = json.loads(f.read())
        self.crypt = hashlib.md5()
        self.sessions = {}

    def login(self, uname, hashedpwd):
        if self.db.get(uname) and self.db[uname]['password'] == hashedpwd:
            self.crypt.update(str.encode(
                f'{time.time()}{uname}', encoding='utf-8'))
            self.sessions[uname] = self.crypt.hexdigest()
            return self.sessions[uname]
        else:
            return None

    def verify_login(self, uname, sessionid):
        if self.sessions.get(uname) and self.sessions[uname] == sessionid:
            return True
        return False

    def logout(self, uname, sessionid):
        if not self.sessions.get(uname):
            return True
        if self.verify_login(uname, sessionid):
            del self.sessions[uname]
            return True
        return False

    def get_user_info(self, uname, sessionid):
        if self.verify_login(uname, sessionid):
            dict_uinfo = copy.deepcopy(self.db[uname])
            del dict_uinfo['password']
            return dict_uinfo
        return None
