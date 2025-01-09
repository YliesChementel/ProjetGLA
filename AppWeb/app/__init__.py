from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

def schedule_alerts(app):
    from .alertes import check_new_crypto_data  # Importer après les configurations de db sinon bug
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_new_crypto_data, trigger="interval", seconds=10, args=[app])
    scheduler.start()
 

# Initialisation de SQLAlchemy
db = SQLAlchemy()

def create_app(config_name):

    load_dotenv()

    app = Flask(__name__)
    
    # Charger la configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True

    if config_name == 'user':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # désactive les modifications inutiles
    
    # Initialiser l'extension SQLAlchemy avec l'application Flask
    db.init_app(app)
    
    # Initialiser Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.Connexion'  

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Récupérer l'utilisateur depuis la base de données par son ID

    # Importer les routes
    from .routes import main
    app.register_blueprint(main)

    schedule_alerts(app)

    return app
