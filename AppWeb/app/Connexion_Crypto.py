import sqlite3
from .models import db, Crypto
import os
from dotenv import load_dotenv


def get_db_connection():
    load_dotenv()
    """Retourne une connexion à la base de données."""
    db_path = os.getenv('DB_PATH', '../instance/Crypto.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_crypto():
    """Récupère les données de la table Crypto depuis la base de données."""
    with get_db_connection() as conn:  # Utilisation de 'with' pour gérer automatiquement la fermeture de la connexion
        return conn.execute('SELECT * FROM Crypto').fetchall()

def getAllcrypto_data():
    """Récupère les données de la table CryptoData depuis la base de données."""
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM CryptoData').fetchall()

def get_crypto_data(id, start_date=None, end_date=None):
    """Récupère les données de CryptoData pour un ID donné avec des filtres sur la date."""
    query = "SELECT * FROM CryptoData WHERE crypto_id = ?"
    params = [id]
    
    if start_date:
        query += " AND fetchTime >= ?"
        params.append(start_date.strftime('%Y/%m/%d %H:%M:%S'))  # Format de la date comme 'YYYY/MM/DD HH:MM:SS'
    
    with get_db_connection() as conn:  # Connexion dans un bloc 'with'
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_last_data():
    """Récupère les dernières données de CryptoData pour les 10 dernières cryptos."""
    crypto_data = get_crypto()
    cryptoData_data = getAllcrypto_data()
    latest_data = {}

    # Trier cryptoData par date (timestamp) et obtenir le dernier prix pour les 10 dernières cryptos
    for data in cryptoData_data[-10:]:
        latest_data[data['crypto_id']] = data

    # Créer un tableau de résultats en associant les cryptomonnaies avec leur dernier prix
    table = []
    for c in crypto_data:
        crypto_id = c['id']
        if crypto_id in latest_data:
            table.append({
                'crypto_id': c['id'],
                'name': c['name'],
                'symbol': c['symbol'],
                'price': latest_data[crypto_id]['price'],
                'volume': latest_data[crypto_id]['volume'],
                'marketCap': latest_data[crypto_id]['marketCap'],
                'rank': latest_data[crypto_id]['rank']
            })

    return table



def populate_crypto_table():
    """Remplir la table Crypto dans la base SQLAlchemy avec les données de la base SQLite."""
    # Récupérer les données de la table 'Crypto' dans la base SQLite
    crypto_data = get_crypto()
    
    # Obtenir toutes les cryptos existantes dans la base SQLAlchemy
    existing_cryptos = {crypto.symbol for crypto in Crypto.query.all()}

    # Ajouter les cryptos manquantes
    new_cryptos = []
    for crypto in crypto_data:
        if crypto['symbol'] not in existing_cryptos:
            new_crypto = Crypto(
                id=crypto['id'],
                symbol=crypto['symbol'],
                name=crypto['name']
            )
            new_cryptos.append(new_crypto)

    # Si de nouvelles cryptos existent, les ajouter à la session
    if new_cryptos:
        db.session.add_all(new_cryptos)
        db.session.commit()
