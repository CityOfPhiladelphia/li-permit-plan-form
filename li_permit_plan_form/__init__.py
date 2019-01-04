from flask import Flask, render_template

from config import SECRET_KEY
from li_permit_plan_form import form, plans, search
from li_permit_plan_form.db import close_db


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(form.bp)
    app.register_blueprint(plans.bp)
    app.register_blueprint(search.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

def init_app(app):
    app.teardown_appcontext(close_db)