provider "aws" {
    region = "eu-west-2"
}

data "aws_iam_role" "execution-role" {
    name = "ecsTaskExecutionRole"
}

# create the bucket and configure its settings
resource "aws_s3_bucket" "plant-bucket" {
  bucket = "c9-queenbees-bucket"
  object_lock_enabled = false
}

resource "aws_s3_bucket_public_access_block" "plant-bucket-public-access" {
  bucket = aws_s3_bucket.plant-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "plany-bucket-versioning" {
  bucket = aws_s3_bucket.plant-bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "plant-bucket-encryption" {
  bucket = aws_s3_bucket.plant-bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
    bucket_key_enabled = true
  }
}

# TODO: change the image string to the appropriate image in the ECR for all task definitions
# Also, configure the environment properly

# task definition for pipeline that extracts from API and uploads to RDS
resource "aws_ecs_task_definition" "plant-pipeline-task-def" {
    family = "c9-queenbees-plant-pipeline-taskdef"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    container_definitions = jsonencode([
        {
            name: "pipeline"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-queenbees-plant-pipeline-repo:dummy"
            essential: true
            environment: [
                { name: "DB_NAME", value: var.DB_NAME },
                { name: "DB_HOST", value: var.DB_HOST },
                { name: "DB_PASSWORD", value: var.DB_PASSWORD },
                { name: "DB_USERNAME", value: var.DB_USERNAME },
                { name: "DB_PORT", value: var.DB_PORT }
            ]
        }
    ])
    execution_role_arn = data.aws_iam_role.execution-role.arn
    memory = 2048
    cpu = 1024
}

# task definition for pipeline that extracts from RDS and uploads to the S3
resource "aws_ecs_task_definition" "rds-pipeline-task-def" {
    family = "c9-queenbees-rds-s3-pipeline-taskdef"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    container_definitions = jsonencode([
        {
            name: "pipeline"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-queenbees-s3-pipeline-repo:dummy"
            essential: true
            environment: [
                { name: "DB_NAME", value: var.DB_NAME },
                { name: "DB_HOST", value: var.DB_HOST },
                { name: "DB_PASSWORD", value: var.DB_PASSWORD },
                { name: "DB_USERNAME", value: var.DB_USERNAME },
                { name: "DB_PORT", value: var.DB_PORT }
            ]
        }
    ])
    execution_role_arn = data.aws_iam_role.execution-role.arn
    memory = 2048
    cpu = 1024
}

# task definition for dashboard
resource "aws_ecs_task_definition" "dashboard-task-def" {
    family = "c9-quuenbees-dashboard-taskdef"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    container_definitions = jsonencode([
        {
            name: "dashboard"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-queenbees-dashboard-repo:dummy"
            essential: true
            portMappings: [{
                containerPort = 8501
                hostPort = 8501
            }]
            environment: [
                { name: "DB_NAME", value: var.DB_NAME },
                { name: "DB_HOST", value: var.DB_HOST },
                { name: "DB_PASSWORD", value: var.DB_PASSWORD },
                { name: "DB_USERNAME", value: var.DB_USERNAME },
                { name: "DB_PORT", value: var.DB_PORT }
            ]
        }
    ])
    execution_role_arn = data.aws_iam_role.execution-role.arn
    memory = 2048
    cpu = 1024
}

resource "aws_security_group" "allow-dashboard-access" {
  name        = "c9-queenbees-dashboard-sg"
  description = "Allow outbound traffic for port 8501, so users can see the dashboard"
  vpc_id      = "vpc-04423dbb18410aece"

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}