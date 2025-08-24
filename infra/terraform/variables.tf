variable "name" { 
    type = string 
    default = "lead-scorer"
     }
variable "aws_region" { 
    type = string 
    default = "us-east-1" 
    }
variable "desired_count" { 
    type = number 
    default = 2 
    }
variable "task_cpu" { 
    type = number 
    default = 512 
    }
variable "task_memory" { 
    type = number 
    default = 1024 
    }
