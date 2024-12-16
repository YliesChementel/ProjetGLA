from locust import HttpUser, task, between

class MyUser(HttpUser):
    # Temps d'attente entre chaque tâche (en secondes)
    wait_time = between(1, 3)  # attendre entre 1 et 3 secondes après chaque tâche

    # Définition de la tâche à exécuter
    @task
    def get_homepage(self):
        self.client.get("/")  # Faire une requête GET à la page d'accueil

    @task(3)  # Cette tâche a 3 fois plus de poids que la précédente
    def view_item(self):
        self.client.get("/item/1")  # Faire une requête GET à une page d'item
