# Operations

## Deploy
- Push to `main` triggers CI; image pushed to ECR; Terraform applies to staging.
- For prod, protect with an approval job and blue/green shift using a second target group.

## Runbook
- **Health**: `/healthz`, `/readyz`
- **High error rates**: Check CloudWatch Logs, ECS events, ALB 5xx count
- **Latency spikes**: Inspect p99 alarm, scale out ECS desired count, verify external dependencies (SageMaker, Snowflake)
- **Secrets**: Rotated in AWS Secrets Manager (CI uses OIDC)