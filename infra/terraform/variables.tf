##############################
# General Variables
##############################

variable "name" {
  description = "Base name for resources (prefix)"
  type        = string
  default     = "lead-scorer"
}

variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "us-east-1"
}

##############################
# ECS Task Settings
##############################

variable "task_cpu" {
  description = "CPU units for the ECS task"
  type        = number
  default     = 256 # ~0.25 vCPU
}

variable "task_memory" {
  description = "Memory (in MiB) for the ECS task"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Number of ECS tasks to run"
  type        = number
  default     = 2
}

##############################
# VPC Settings
##############################

variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "Public subnet CIDRs"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "Private subnet CIDRs"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}
