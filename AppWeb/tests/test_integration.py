import pytest
from unittest import mock
import smtplib
from app.alertes import *
from app.models import Alerte  
from flask import Flask
from unittest.mock import patch
from app import create_app, db
from app.models import User,Crypto, Alerte
from unittest.mock import patch
from flask import url_for


@pytest.fixture
def mock_send_email():
    with patch('app.alertes.send_email') as mock_send_email:
        yield mock_send_email

@pytest.fixture
def client(app):
    """Fixture pour fournir un client de test Flask."""
    return app.test_client()

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'  # Add a secret key for tests
    app = create_app('testing')
    with app.app_context():
        db.create_all()  # Create the database for testing
        yield app
        db.drop_all()  # Clean up the database after tests
    return app


@pytest.fixture
def new_user(app):
    with app.app_context():  
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
    return user

@pytest.fixture
def new_crypto(app):
    with app.app_context():  
        # Créer une instance de Crypto
        crypto = Crypto(id='1', symbol='BTC', name='Bitcoin')
        db.session.add(crypto)
        db.session.commit()
    return crypto

@pytest.fixture
def new_alert(new_user, new_crypto, app):
    with app.app_context():
        # Réattacher les objets User et Crypto à la session
        user = db.session.merge(new_user)
        crypto = db.session.merge(new_crypto)
        
        alerte = Alerte(user_id=user.id, crypto_id=crypto.id, condition='price', threshold_value=10000.0, type_alert='greater_than', time=10)
        db.session.add(alerte)
        db.session.commit()
    return alerte





def test_create_alerte_and_send_email(client, new_user, new_crypto,new_alert, mock_send_email,app):
    """Test d'intégration pour la création d'une alerte et l'envoi d'un email"""
    with app.app_context():
        new_user = db.session.merge(new_user)
        new_crypto = db.session.merge(new_crypto)


    # Créer une alerte via une requête POST
    response = client.post('/Alertes', data={
            'crypto_id': new_crypto.id,
            'condition': 'price',
            'threshold_value': 10000.0,
            'type_alert': 'greater_than',
            'time': 10
        })
    
    assert response.status_code == 302 
    
    with app.app_context():
        new_alert =  db.session.merge(new_alert)

    # Simuler une mise à jour de la valeur de la crypto
    current_value = 12000.0
    alert_type = 'greater_than'
    
    # Appeler la fonction qui traite l'alerte et envoie un email
    with app.app_context():
        new_alert =  db.session.merge(new_alert)
        send_email_alert(new_alert, current_value, alert_type) 

    # Vérifier que la fonction d'envoi d'email a été appelée
    mock_send_email.assert_called_once_with(
        'Alerte pour Bitcoin - greater_than',
        'Alerte pour Bitcoin - Valeur: 12000.0 (type inconnu)',
        new_user.email
    )



def test_create_and_authenticate_user(client):
    """Test d'intégration pour la création et l'authentification d'un utilisateur"""
    
    # Créer un utilisateur via une requête POST
    response = client.post('/Inscription', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    
    assert response.status_code == 302    # 302 == redirection

    response = client.post('/Connexion', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    assert response.status_code == 302    # 302 == redirection
    assert response.location == '/'  # Vérifie la redirection vers la page d'accueil