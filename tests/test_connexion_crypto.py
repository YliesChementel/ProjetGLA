import sqlite3
from app.Connexion_Crypto import *

def test_get_db_connection():
    conn = get_db_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()



def test_get_crypto_data():
    data = get_crypto_data("BTC")
    assert data is not None
    assert isinstance(data, list)

def test_get_crypto_data_invalid_id():
    data = get_crypto_data("INVALID_ID")
    assert data == []


def test_get_crypto():
    data = get_crypto()
    assert data is not None
    assert isinstance(data, list)


def test_getAllcrypto_data():
    data = getAllcrypto_data()
    assert data is not None
    assert isinstance(data, list)
    
    
def test_get_last_data():
    data = get_last_data()
    assert data is not None
    assert isinstance(data, list)

