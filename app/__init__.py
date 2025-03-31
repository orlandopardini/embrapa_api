from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    Swagger(app)  # <- Aqui ativamos a documentação Swagger

    return app