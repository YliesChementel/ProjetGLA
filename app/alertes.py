from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from .models import  db, Alerte  
from .sendEmail import send_email
from .DbConnexion import get_crypto_data, get_db_connection


#Fonction pour vérifier les nouvelles données dans CryptoData
def check_new_crypto_data(app):
    # Connexion à la base de données 'CryptoData'
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query pour récupérer les nouvelles entrées depuis CryptoData (ajuster la logique selon ta table)
    date = datetime.now() - timedelta(seconds=5)
    date = date.strftime('%Y/%m/%d %H:%M:%S')
    cursor.execute("SELECT * FROM CryptoData WHERE fetchTime > ?", (date,))  # Par exemple, les données des 5 dernières secondes
    new_data = cursor.fetchall()

    if new_data:
        print(f"Nouvelles données détectées")
        for row in new_data:
            check_alerts(app)

    conn.close()


def check_alerts(app):
    with app.app_context():  # Utilisation du contexte d'application
        alertes = Alerte.query.options(joinedload(Alerte.user),joinedload(Alerte.crypto)).all()

    for alerte in alertes:
        # Récupérer les données récentes de la cryptomonnaie
        crypto_data = get_crypto_data(alerte.crypto_id)
        
        # Vérifier si l'alerte doit être déclenchée
        if alerte.condition == 'prix':
            current_price = crypto_data[-1]['price']  # Dernier prix
            if alerte.type_alert == 'greater_than' and current_price > alerte.threshold_value:
                send_email_alert(alerte, current_price)
            elif alerte.type_alert == 'less_than' and current_price < alerte.threshold_value:
                send_email_alert(alerte, current_price,"prix")
        if alerte.condition == 'Volume':
            current_volume = crypto_data[-1]['volume']  # Dernier volume

            if alerte.type_alert == 'greater_than' and current_volume > alerte.threshold_value:
                send_email_alert(alerte, current_volume, 'volume')
            elif alerte.type_alert == 'less_than' and current_volume < alerte.threshold_value:
                send_email_alert(alerte, current_volume, 'volume')
        if alerte.condition == 'marketCap':
            current_market_cap = crypto_data[-1]['marketCap']  # Dernière capitalisation

            if alerte.type_alert == 'greater_than' and current_market_cap > alerte.threshold_value:
                send_email_alert(alerte, current_market_cap, 'marketCap')
            elif alerte.type_alert == 'less_than' and current_market_cap < alerte.threshold_value:
                send_email_alert(alerte, current_market_cap, 'marketCap')
        elif alerte.condition == 'percentage':
            # Calculer la variation en pourcentage entre le prix actuel et le prix précédent
            current_price = crypto_data[-1]['price']
            previous_price = crypto_data[-2]['price']
            price_change_percentage = ((current_price - previous_price) / previous_price) * 100

            if alerte.type_alert == 'greater_than' and price_change_percentage > alerte.threshold_value:
                send_email_alert(alerte, price_change_percentage, 'percentage')
            elif alerte.type_alert == 'less_than' and price_change_percentage < alerte.threshold_value:
                send_email_alert(alerte, price_change_percentage, 'percentage')

        

def send_email_alert(alerte, current_value, alert_type):
    # Envoyer un email à l'utilisateur
    user = alerte.user
    subject = f"Alerte pour {alerte.crypto.name} - {alert_type}"
    if alert_type == 'price':
        body = f"Le prix de {alerte.crypto.name} est maintenant de {current_value}."
    elif alert_type == 'volume':
        body = f"Le volume de {alerte.crypto.name} est maintenant de {current_value}."
    elif alert_type == 'marketCap':
        body = f"La capitalisation boursière de {alerte.crypto.name} est maintenant de {current_value}."
    elif alert_type == 'percentage':
        body = f"La variation en pourcentage du prix de {alerte.crypto.name} est maintenant de {current_value}%."

    send_email(subject, body, user.email)