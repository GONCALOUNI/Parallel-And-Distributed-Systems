import random
import string
from locust import HttpUser, between, task

def random_key(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

class KVUser(HttpUser):
    wait_time = between(0.1, 1)

    @task(3)
    def put_item(self):
        k = random_key()
        self.client.put("/kv",
            json={"key": k, "value": "val_"+k},
            headers={"Content-Type":"application/json"}
        )

    @task(5)
    def get_item(self):
        self.client.get(f"/kv?key={random_key()}")

    @task(2)
    def delete_item(self):
        k = random_key()
        self.client.put("/kv", json={"key":k,"value":"v"})
        self.client.delete(f"/kv?key={k}")