from flask_httpauth import HTTPDigestAuth

from config import users


auth = HTTPDigestAuth()

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None