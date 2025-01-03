from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler



# Initialisation de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Charger la configuration
    app.config['SECRET_KEY'] = 'your_secret_key'
    # Configurer la base de données utilisateur
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Utilisateur.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # désactive les modifications inutiles
    
    # Initialiser l'extension SQLAlchemy avec l'application Flask
    db.init_app(app)
    
    # Initialiser Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.Connexion'  # Nom de la route de connexion

    from .models import User  # Importer le modèle utilisateur

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Récupérer l'utilisateur depuis la base de données par son ID

    # Importer les routes
    from .routes import main
    app.register_blueprint(main)

    #from .alertes import check_new_crypto_data  # Importer après les configurations de db sinon bug
    #scheduler = BackgroundScheduler()
    #scheduler.add_job(func=check_new_crypto_data, trigger="interval", seconds=5, args=[app])  # Passer l'argument 'crypto_id' via 'args'
    #scheduler.start()

    return app
