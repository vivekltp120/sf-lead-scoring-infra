host_url="https://786gud1i14.execute-api.us-east-1.amazonaws.com/serving_lead_score/predictor-lambda"
curl -X POST $host_url -H "Content-Type: application/json" -d @test-input.json
