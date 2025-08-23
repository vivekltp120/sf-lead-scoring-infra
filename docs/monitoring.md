# Monitoring & Alerts

- **System**: ALB 5xx, TargetResponseTime p99, ECS CPU/Memory target tracking
- **App Metrics**: request counts, latencies (Prometheus), success/error counts
- **ML Metrics**: Input feature drift (KS distance), score distribution drift, data quality checks (nulls, ranges)
- **Alerting**: CloudWatch Alarms -> SNS -> Slack/Email
