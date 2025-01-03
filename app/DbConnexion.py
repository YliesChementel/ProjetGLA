import sqlite3
from .models import db, Crypto

def get_db_connection():
    """Retourne une connexion à la base de données."""
    conn = sqlite3.connect('instance/Crypto.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_crypto():
    """Récupère les données de la table Crypto depuis la base de données."""
    conn = get_db_connection()
    crypto_data = conn.execute('SELECT * FROM Crypto').fetchall()
    conn.close()
    return crypto_data

def getAllcrypto_data():
    """Récupère les données de la table CryptoData depuis la base de données."""
    conn = get_db_connection()
    cryptoData_data = conn.execute('SELECT * FROM CryptoData').fetchall()
    conn.close()
    return cryptoData_data

def get_crypto_data(id, start_date=None, end_date=None):
    conn = get_db_connection()  # Connexion à la base de données
    cursor = conn.cursor()
    query = f"SELECT * FROM CryptoData WHERE crypto_id = ?"
    params = [id]
    
    if start_date:
        query += " AND fetchTime >= ?"
        params.append(start_date.strftime('%Y/%m/%d %H:%M:%S'))  # Format de la date comme 'YYYY/MM/DD HH:MM:SS'
    
    cursor.execute(query, params)
    cryptoData_data = cursor.fetchall()
    
    conn.close()
    return cryptoData_data

def get_last_data():
    crypto_data=get_crypto()
    cryptoData_data=getAllcrypto_data()
    latest_data = {}

    # Trier cryptoData par date (timestamp) et obtenir le dernier prix pour chaque crypto
    for data in cryptoData_data:
        crypto_id = data['crypto_id']
        price = data['price']
        # Si ce crypto_id n'est pas encore dans le dictionnaire ou que le timestamp est plus récent
        if crypto_id not in latest_data or data['fetchTime'] > latest_data[crypto_id]['fetchTime']:
            latest_data[crypto_id] = data


    # 2. Créer un tableau de résultats en associant les cryptomonnaies avec leur dernier prix
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
                'marketCap':latest_data[crypto_id]['marketCap'],
                'rank': latest_data[crypto_id]['rank']
            })
    # Trier le tableau par rang (rank) ou tout autre critère, ici c'est trié par 'rank' pour l'exemple
    table = sorted(table, key=lambda x: x['rank'])

    # Limiter à 10 éléments
    return table[:10]        




def populate_crypto_table():
    """Remplir la table Crypto dans la base SQLAlchemy avec les données de la base SQLite."""
    # Récupérer les données de la table 'Crypto' dans la base SQLite
    crypto_data = get_crypto()
    
    # Pour chaque crypto dans la base SQLite, on l'ajoute à la base SQLAlchemy
    for crypto in crypto_data:
        # Vérifier si la crypto existe déjà dans la base SQLAlchemy
        existing_crypto = Crypto.query.filter_by(symbol=crypto['symbol']).first()
        
        # Si la crypto n'existe pas, on l'ajoute
        if not existing_crypto:
            new_crypto = Crypto(
                id=crypto['id'],
                symbol=crypto['symbol'],
                name=crypto['name']
            )
            db.session.add(new_crypto)
    
    # Commit des changements dans la base SQLAlchemy
    db.session.commit()
