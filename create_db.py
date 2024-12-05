from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)

app.config.from_object('config')

# Inicializació de SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.drop_all()
    db.create_all()  
    print("Taules creades a la base de dades")