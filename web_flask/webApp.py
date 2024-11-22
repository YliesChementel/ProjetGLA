from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    connCrypto = sqlite3.connect('Crypto.db')  
    connCryptoData = sqlite3.connect('CryptoData.db')  
    
    connCrypto.row_factory = sqlite3.Row
    connCryptoData.row_factory = sqlite3.Row
    
    crypto_data = connCrypto.execute('SELECT * FROM Crypto').fetchall()
    cryptoData_data = connCryptoData.execute('SELECT * FROM CryptoData').fetchall()
 
    connCrypto.close()
    connCryptoData.close()
    
    return render_template('index.html', crypto_data=crypto_data,cryptoData_data=cryptoData_data)

if __name__ == '__main__':
    app.run(debug=True)