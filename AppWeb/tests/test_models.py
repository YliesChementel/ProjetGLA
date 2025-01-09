import pytest
from datetime import datetime
from werkzeug.security import check_password_hash
from app import create_app, db
from app.models import User, Crypto, Alerte

@pytest.fixture
def app():
    # Configuration de l'application pour les tests
    app = create_app('testing')
    with app.app_context():
        db.create_all()  # Créer la base de données pour les tests
        yield app
        db.drop_all()  # Nettoyer la base de données après les tests

@pytest.fixture
def client(app):
    return app.test_client()

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
def new_alerte(new_user, new_crypto, app):
    with app.app_context():
        # Réattacher les objets User et Crypto à la session
        user = db.session.merge(new_user)
        crypto = db.session.merge(new_crypto)
        
        alerte = Alerte(user_id=user.id, crypto_id=crypto.id, condition='price', threshold_value=10000.0, type_alert='greater_than', time=10)
        db.session.add(alerte)
        db.session.commit()
    return alerte


def test_set_password(new_user):
    """Test la méthode set_password pour l'utilisateur"""
    user = new_user
    user.set_password('newpassword')
    assert check_password_hash(user.password, 'newpassword')


def test_check_password(new_user,app):
    """Test la méthode check_password pour l'utilisateur"""
    with app.app_context():
        # Ensure that the user is attached to the session by merging it
        user = db.session.merge(new_user)  # This will reattach the user to the session
        assert user.check_password('testpassword')
        assert not user.check_password('wrongpassword')

def test_create_user(new_user,app):
    """Test de la création d'un utilisateur"""
    with app.app_context():
        user = db.session.merge(new_user)
        assert user.username == 'testuser'
        assert user.email == 'testuser@example.com'



def test_create_crypto(new_crypto,app):
    """Test de la création d'une crypto"""
    with app.app_context():
        crypto = db.session.merge(new_crypto)
        assert crypto.symbol == 'BTC'
        assert crypto.name == 'Bitcoin'





def test_repr_user(new_user,app):
    """Test de la méthode __repr__ de User"""
    with app.app_context():
        user = db.session.merge(new_user)
        assert repr(user) == '<User testuser>'


def test_repr_crypto(new_crypto,app):
    """Test de la méthode __repr__ de Crypto"""
    with app.app_context():
        crypto = db.session.merge(new_crypto)
        assert repr(crypto) == '<Crypto Bitcoin (BTC)>'


def test_create_alerte(new_alerte,app):
    with app.app_context():
        alerte = db.session.merge(new_alerte)
        assert alerte.condition == 'price'
        assert alerte.threshold_value == 10000.0
        assert alerte.type_alert == 'greater_than'
        assert alerte.time == 10


def test_alerte_relationship(new_alerte, new_user, new_crypto, app):
    """Test des relations entre Alerte, User, et Crypto"""
    with app.app_context():
        new_user = db.session.merge(new_user)
        new_crypto = db.session.merge(new_crypto)
        alerte = db.session.merge(new_alerte)

        assert alerte.user == new_user
        assert alerte.crypto == new_crypto
        assert new_user.alertes[0] == alerte
        assert new_crypto.alertes[0] == alerte


def test_repr_alerte(new_alerte,app):
    """Test de la méthode __repr__ de Alerte"""
    with app.app_context():
        alerte = db.session.merge(new_alerte)
        assert repr(alerte) == '<Alerte 1 for Bitcoin - price>'
