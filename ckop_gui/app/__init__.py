import os

from flask import Flask, render_template

from app.routes import route
from app.config import config, init_config

def create_flask_app():
    app = Flask(__name__)

    route(app)

    # path = os.environ.get('CONFIG_PATH') if os.environ.get(
    #     'CONFIG_PATH') else "./settings.ini"
    # init_config(path)
    # try:
    #     app.config.update(dict(
    #         SECRET_KEY=str(config['FLASK_APP']['FLASK_APP_SECRET_KEY'])
    #     ))
    #     print(f"\n\033[32m Сервер запустился с конфигом:\n\033[32m {path}\n")
    # except KeyError:
    #     print(f"\033[31m Файл {path} не найден или неверный")
    app.config.SECRET_KEY = "sdfsdfsdf"
    app.secret_key = "sdfsdfsdf"
    return app


