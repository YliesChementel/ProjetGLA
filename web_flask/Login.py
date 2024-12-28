from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Configurer la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Utilisez SQLite ou votre base de données préférée

db = SQLAlchemy(app)

# Configuration de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique pour chaque utilisateur
    username = db.Column(db.String(150), unique=True, nullable=False)  # Nom d'utilisateur unique
    password = db.Column(db.String(150), nullable=False)  # Mot de passe sécurisé

    def __repr__(self):
        return f'<User {self.username}>'

# Créer la base de données
with app.app_context():
    db.create_all()  # Crée les tables dans la base de données

def add_user(username, password):
    with app.app_context():
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            print("Cet utilisateur existe déjà.")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            print("Utilisateur ajouté avec succès.")

# Appeler la fonction pour ajouter un utilisateur
add_user('ylies', 'securepassword')

# Liste tous les utilisateurs dans la base de données
with app.app_context():
    users = User.query.all()  # Récupère tous les utilisateurs
    for user in users:
        print(user.username)

if __name__ == '__main__':
    app.run(debug=True)