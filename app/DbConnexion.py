import sqlite3

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
    return table        