from locust import HttpUser, task, between
import json
import numpy as np
host_url="https://786gud1i14.execute-api.us-east-1.amazonaws.com/serving_lead_score/predictor-lambda"

class LeadScoringUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def score_lead(self):
        # Example random payload with 50 features
        num_samples = 1                 # Number of samples you want to predict
        num_features = 50                     # Number of features per sample

      
        # Example: generate random data; replace with your actual input
        data = np.random.rand(num_samples,num_features).tolist()

        lead_data={"input_data":data}        
        self.client.post(
            url= host_url,
            body=json.dumps(lead_data),
            headers={"Content-Type": "application/json"}
        )
