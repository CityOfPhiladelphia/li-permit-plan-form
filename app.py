from flask import Flask, request, g, flash, render_template
from config import SECRET_KEY
from db import close_db
from auth import requires_auth
# from gevent.pywsgi import WSGIServer


app = Flask(__name__)
# Close the database when the app shuts down
app.teardown_appcontext(close_db)
app.secret_key = SECRET_KEY

@requires_auth
@app.route('/')
def index():
    return render_template('index.html')

@requires_auth
@app.route('/search')
def search():
    return render_template('search.html')

@requires_auth
@app.route('/form')
def form():
    return render_template('form.html')

    

# if __name__ == '__main__':
#     http_server = WSGIServer(('0.0.0.0', 8100), app)
#     http_server.serve_forever()