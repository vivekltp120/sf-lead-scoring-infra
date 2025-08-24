from locust import HttpUser, task, between
import random
import json

class LeadScoringUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def score_lead(self):
        # Example random payload with 50 features
        payload = {
            "lead_id": "123",
            "features":{ 
            f"f_{i}": random.random()
            for i in range(50)
            }

        }
        self.client.post(
            "/score", 
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
