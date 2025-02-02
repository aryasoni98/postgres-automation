variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "postgresql_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "14"
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
}

variable "bastion_cidr" {
  description = "CIDR block for bastion host access"
  type        = string
}
