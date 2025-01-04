from locust import HttpUser, task, between

class CryptoUser(HttpUser):
    wait_time = between(1, 3)  # Attente entre les requêtes

    @task
    def index(self):
        self.client.get("/")

    @task
    def list_crypto(self):
        self.client.get("/ListeCrypto")

    @task
    def graph_crypto(self):
        self.client.get("/GraphCrypto?id=bitcoin")