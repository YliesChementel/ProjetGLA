from locust import HttpUser, task, between, SequentialTaskSet
import random
from time import sleep


class CryptoUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        """Test de la page d'accueil"""
        self.client.get("/")

    @task
    def list_crypto(self):
        """Test de la page de la liste des cryptomonnaies"""
        self.client.get("/ListeCrypto")

    @task
    def graph_crypto(self):
        """Test d'une page de graphique avec une crypto particulière"""
        choice = ['bitcoin','ethereum','tether']  
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
        choice = ['bitcoin','ethereum','tether']  
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


