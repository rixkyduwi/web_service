# curl -H "Authorization: Bearer secret-token-1" http://127.0.0.1:7001/

from flask import Flask
from flask_httpauth import HTTPTokenAuth


app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# nama kelompok 
# rizky dwi saputra (6A) 
# muh saefudin fikri (6B) 
tokens = {
    "secret-token-1": "19090107",
    "secret-token-2": "19090101"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/api/v2/users/info')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug = True, port=4000)