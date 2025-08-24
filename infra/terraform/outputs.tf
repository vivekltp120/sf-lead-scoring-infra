output "ecr_url" { 
    value = aws_ecr_repository.api.repository_url
     }
output "alb_dns_name" { 
    value = module.alb.this_lb_dns_name 
    }
