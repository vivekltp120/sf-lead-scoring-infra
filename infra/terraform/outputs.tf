##############################
# ALB Outputs
##############################

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.dns_name
}

output "alb_arn" {
  description = "ARN of the ALB"
  value       = module.alb.arn
}

output "alb_arn_suffix" {
  description = "ARN suffix of the ALB (for CloudWatch metrics)"
  value       = module.alb.arn_suffix
}

##############################
# Target Group Outputs
##############################

output "target_group_arn" {
  description = "ARN of the ECS target group"
  value       = aws_lb_target_group.api.arn
}

##############################
# ECS Outputs
##############################

output "ecs_cluster_id" {
  description = "ECS Cluster ID"
  value       = module.ecs.cluster_id
}

output "ecs_service_name" {
  description = "ECS Service name"
  value       = aws_ecs_service.api.name
}

output "ecs_task_definition" {
  description = "Task definition ARN for ECS service"
  value       = aws_ecs_task_definition.api.arn
}

##############################
# ECR Outputs
##############################

output "ecr_repository_url" {
  description = "ECR repository URL for pushing images"
  value       = aws_ecr_repository.api.repository_url
}
