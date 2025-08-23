# Scope Decisions

- Provision a minimal yet realistic **ECS Fargate** + **ALB** stack to control costs.
- Use a **mock XGBoost-compatible scorer** to keep local runs fully reproducible without large binaries.
- Provide **Terraform** that teams can extend with Cognito, PrivateLink to SageMaker/Snowflake, and VPC endpoints.
- CI includes **security gates** but does not fail hard on image scan in demo mode (set exit-code to 0). In prod, enable blocking.
