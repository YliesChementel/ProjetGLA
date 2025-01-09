from locust import HttpUser, task, between, SequentialTaskSet
import random
from time import sleep
from app.Connexion_Crypto import get_crypto
import os
from dotenv import load_dotenv

class CryptoUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        """Test de la page d'accueil"""
        self.client.get("/")

    @task
    def list_crypto(self):
        """Test de la page de la liste des cryptomonnaies"""
        db_path = os.getenv('DB_PATH', '../instance/Crypto.db')
        print("test    :    ",db_path)
        if not os.path.exists(db_path):
            print(f"Warning: The database path '{db_path}' does not exist!")
        self.client.get("/ListeCrypto")

    @task
    def graph_crypto(self):
        """Test d'une page de graphique avec une crypto particulière"""
        crypto_data = get_crypto()
        choice = [c['id'] for c in crypto_data]  
        crypto_id = random.choice(choice)
        time = [None,'1h','12h','1d','7d']
        time_random = random.choice(time)
        self.client.get(f"/GraphCrypto?id={crypto_id}&time_range={time_random}")

    @task
    def login(self):
        """Test de la page de connexion"""
        self.client.get("/Connexion")

        self.client.post("/Connexion", data={
            "username": "test",
            "password": "test"
        })

    @task
    def signup(self):
        """Test de la page d'inscription"""
        self.client.get("/Inscription")

        self.client.post("/Inscription", data={
            "username": f"test",
            "email": f"test",
            "password": "test"
        })

    @task
    def profil(self):
        """Accéder à la page du profil utilisateur"""
        self.client.get("/profil")
        sleep(1)


class UserBehavior(SequentialTaskSet):
    """Exécuter une séquence d'actions pour simuler un comportement utilisateur"""
    
    @task
    def execute_tasks(self):
        self.client.get("/")
        sleep(2)
        self.client.get("/ListeCrypto")
        sleep(2)
        crypto_data = get_crypto()
        choice = [c['id'] for c in crypto_data]  
        crypto_id = random.choice(choice)
        self.client.get(f"/GraphCrypto?id={crypto_id}")
        sleep(2)
        self.client.get("/Connexion")
        sleep(1)
        self.client.get("/Inscription")
        sleep(1)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)


