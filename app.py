import os
from flask_admin import Admin
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, flash, redirect, url_for


from models import db, User, Wine, Profile, UserInfo, Compras
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
    
    # Set up Flask-Admin
    admin = Admin(app, name='MyAdmin', template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Wine, db.session))
    admin.add_view(ModelView(Profile, db.session))
    admin.add_view(ModelView(UserInfo, db.session))
    admin.add_view(ModelView(Compras, db.session))


    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
        # return User.query.get(int(user_id))
    
    
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("You must log in to access this feature", 'warning')
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