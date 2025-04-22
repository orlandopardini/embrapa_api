from flasgger import Swagger
from flask import Flask
from app.routes import main  # <- Isso importa o blueprint certo

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    Swagger(app)  # <- Aqui ativamos a documentação Swagger
    return app
