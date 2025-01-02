from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Crypto(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Crypto {self.name} ({self.symbol})>'

class Alerte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'), nullable=False)
    condition = db.Column(db.String(150), nullable=False)  # 'price', 'percentage', 'indicator', etc.
    threshold_value = db.Column(db.Float, nullable=False)  # Seuil de l'alerte
    type_alert = db.Column(db.String(50), nullable=False)  # 'greater_than', 'less_than', etc.

    user = db.relationship('User', backref=db.backref('alertes', lazy=True))
    crypto = db.relationship('Crypto', backref=db.backref('alertes', lazy=True))

    def __repr__(self):
        return f'<Alerte {self.id} for {self.crypto.name} - {self.condition}>'

