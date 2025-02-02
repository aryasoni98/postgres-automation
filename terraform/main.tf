provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "selected" {
  id = var.vpc_id
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_security_group" "postgresql" {
  name        = "postgresql-${var.environment}"
  description = "Security group for PostgreSQL instances"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.selected.cidr_block]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.bastion_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "postgresql-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_instance" "primary" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = var.subnet_ids[0]

  vpc_security_group_ids = [aws_security_group.postgresql.id]
  key_name              = var.key_name

  root_block_device {
    volume_size = 100
    volume_type = "gp3"
  }

  tags = {
    Name        = "postgresql-primary-${var.environment}"
    Environment = var.environment
    Role        = "primary"
  }
}

resource "aws_instance" "replica" {
  count         = var.replica_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = var.subnet_ids[count.index % length(var.subnet_ids)]

  vpc_security_group_ids = [aws_security_group.postgresql.id]
  key_name              = var.key_name

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }

  tags = {
    Name        = "postgresql-replica-${count.index + 1}-${var.environment}"
    Environment = var.environment
    Role        = "replica"
  }
}
