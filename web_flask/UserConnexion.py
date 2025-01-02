from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


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