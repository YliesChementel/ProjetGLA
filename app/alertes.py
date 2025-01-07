import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from .Models import  db, Alerte  
from .Connexion_Crypto import get_crypto_data, get_db_connection


def send_email(subject, body, to_email):
    from_email = "cryptofrontiersnotif@gmail.com"
    password = "wgks xsao gjkx npqq "

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Connexion via TLS
        server.starttls()  # Démarrer la connexion TLS
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")


#Fonction pour vérifier les nouvelles données dans CryptoData
def check_new_crypto_data(app):
    # Connexion à la base de données 'CryptoData'
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query pour récupérer les nouvelles entrées depuis CryptoData
    date = datetime.now() - timedelta(seconds=10)
    date = date.strftime('%Y/%m/%d %H:%M:%S')

    cursor.execute("SELECT * FROM CryptoData WHERE fetchTime > ? ORDER BY fetchTime DESC LIMIT 1", (date,))
    new_data = cursor.fetchall()

    if new_data:
        print(f"Nouvelles données détectées")
        # Sélectionne uniquement la dernière ligne des nouvelles données
        last_row = new_data[0]
        print(last_row)
        check_alerts(app)

    conn.close()


def check_alerts(app):
    with app.app_context():  # Utilisation du contexte d'application
        alertes = Alerte.query.options(joinedload(Alerte.user),joinedload(Alerte.crypto)).all()

        for alerte in alertes:
            # Récupérer les données récentes de la cryptomonnaie
            crypto_data = get_crypto_data(alerte.crypto_id)

            # Calculer l'heure actuelle
            now = datetime.now()

            # Vérifier si l'intervalle de temps depuis le dernier envoi est supérieur à l'intervalle défini
            if alerte.last_sent:
                time_diff = now - alerte.last_sent
                if time_diff < timedelta(minutes=alerte.time):
                    continue
            
            # Vérifier si l'alerte doit être déclenchée
            if alerte.condition == 'price':
                current_price = crypto_data[-1]['price']  # Dernier prix
                if alerte.type_alert == 'greater_than' and current_price > alerte.threshold_value:
                    send_email_alert(alerte, current_price,"price")
                elif alerte.type_alert == 'less_than' and current_price < alerte.threshold_value:
                    send_email_alert(alerte, current_price,"price")
            if alerte.condition == 'volume':
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

            alerte.last_sent = now
            db.session.commit()

        
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
    else:
        # Cas par défaut si `alert_type` ne correspond à aucune des valeurs attendues
        body = f"Alerte pour {alerte.crypto.name} - Valeur: {current_value} (type inconnu)"
        print(f"Warning: alert_type '{alert_type}' non reconnu, envoi d'un message générique.")
    send_email(subject, body, user.email)


