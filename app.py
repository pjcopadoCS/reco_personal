import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager

from models import db, User
from user_management import users_bp
from questions import questions_bp
from purchases import purchases_bp


def crear_app():
    app = Flask(__name__)

    app.config.from_object('config')

    app.register_blueprint(users_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(purchases_bp)

    db.init_app(app)
    login_manager = LoginManager(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("Has d'iniciar sessió per accedir a aquesta funcionalitat", 'warning')
        return redirect(url_for('home'))
    
    
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')
    
    return app


app=None
if __name__ == "__main__":
    app = crear_app()
    app.run(debug=True)
else:
    app = crear_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)