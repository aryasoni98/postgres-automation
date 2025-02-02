output "primary_instance_ip" {
  description = "Private IP of primary PostgreSQL instance"
  value       = aws_instance.primary.private_ip
}

output "replica_instance_ips" {
  description = "Private IPs of replica PostgreSQL instances"
  value       = aws_instance.replica[*].private_ip
}

output "primary_instance_id" {
  description = "Instance ID of primary PostgreSQL"
  value       = aws_instance.primary.id
}

output "replica_instance_ids" {
  description = "Instance IDs of replica PostgreSQL instances"
  value       = aws_instance.replica[*].id
}
