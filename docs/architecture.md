# Architecture

- **Client** -> **ALB (WAF)** -> **ECS Fargate (FastAPI)** -> **(Optional) SageMaker Endpoint** for heavy model execution.
- **Observability**: `/metrics` (Prometheus), CloudWatch Logs/Container Insights, example CloudWatch Alarm (p99).
- **Async sink**: Score events -> Kinesis Firehose -> S3 data lake (parquet) for analytics & Model Monitor backfills.
- **Security**: Cognito JWT (documented), Secrets Manager, private subnets, least-privilege IAM.
- **Scalability**: ECS service with target tracking on RPS and CPU; multiple AZs.

### Latency Budget
- Network + ALB: ~30–60ms typical
- App (validation + model call): ~5–15ms for light model; <600ms if remote SageMaker under load
- Total p99 target: <1000ms

### Model Monitoring
- Template for SageMaker Model Monitor (data quality & drift). In the demo, input distributions are logged to S3.
