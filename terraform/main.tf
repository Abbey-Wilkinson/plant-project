provider "aws" {
    region = "eu-west-2"
}

data "aws_iam_role" "execution-role" {
    name = "ecsTaskExecutionRole"
}

data "aws_ecs_cluster" "c9-cluster" {
    cluster_name = "c9-ecs-cluster"
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

# task definition for pipeline that extracts from API and uploads to RDS
resource "aws_ecs_task_definition" "plant-pipeline-task-def" {
    family = "c9-queenbees-plant-pipeline-taskdef"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    container_definitions = jsonencode([
        {
            name: "plant_pipeline"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-queenbees-plant-pipeline-repo:latest"
            essential: true
            environment: [
                { name: "DB_HOST", value: var.DB_HOST },
                { name: "DB_PASSWORD", value: var.DB_PASSWORD },
                { name: "DB_USER", value: var.DB_USER }
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
            name: "rds_s3_pipeline"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-queenbees-s3-pipeline-repo:latest"
            essential: true
            environment: [
                { name: "DB_HOST", value: var.DB_HOST },
                { name: "DB_PASSWORD", value: var.DB_PASSWORD },
                { name: "DB_USER", value: var.DB_USER },
                { name: "AWS_ACCESS_KEY_ID", value: var.AWS_ACCESS_KEY_ID},
                { name: "AWS_SECRET_ACCESS_KEY", value: var.AWS_SECRET_ACCESS_KEY}
            ]
        }
    ])
    execution_role_arn = data.aws_iam_role.execution-role.arn
    memory = 2048
    cpu = 1024
}

# task definition for dashboard
resource "aws_ecs_task_definition" "dashboard-task-def" {
    family = "c9-queenbees-dashboard-taskdef"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    container_definitions = jsonencode([
        {
            name: "dashboard"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-queenbees-dashboard-repo:latest"
            essential: true
            portMappings: [{
                containerPort = 8501
                hostPort = 8501
            }]
            environment: [
                { name: "DB_HOST", value: var.DB_HOST },
                { name: "DB_PASSWORD", value: var.DB_PASSWORD },
                { name: "DB_USER", value: var.DB_USER },
                { name: "AWS_ACCESS_KEY_ID", value: var.AWS_ACCESS_KEY_ID},
                { name: "AWS_SECRET_ACCESS_KEY", value: var.AWS_SECRET_ACCESS_KEY},
                { name: "BUCKET_NAME", value: var.BUCKET_NAME}
            ]
        }
    ])
    execution_role_arn = data.aws_iam_role.execution-role.arn
    memory = 2048
    cpu = 1024
}

# security group to allow inbound traffic on port 8501 for the dashboard
resource "aws_security_group" "dashboard-sg" {
  name        = "c9-queenbees-dashboard-securitygroup"
  description = "Allow inbound traffic for port 8501, so users can see the dashboard"
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
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# start ECS service for the dashboard
resource "aws_ecs_service" "dashboard-service" {
    name = "c9-queenbees-dashboard-service"
    cluster = data.aws_ecs_cluster.c9-cluster.id
    task_definition = aws_ecs_task_definition.dashboard-task-def.arn
    desired_count = 1
    launch_type = "FARGATE"
    network_configuration {
      subnets = ["subnet-0d0b16e76e68cf51b", "subnet-081c7c419697dec52", "subnet-02a00c7be52b00368"]
      security_groups = [aws_security_group.dashboard-sg.id]
      assign_public_ip = true
    }
}

# create a role for the EventBridge schedules
resource "aws_iam_role" "schedule-role" {
    name = "c9-queenbees-schedule-role"
    assume_role_policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "scheduler.amazonaws.com"
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "aws:SourceAccount": "129033205317"
                    }
                }
            }
        ]
    })
}

# create policy for the schedule role
resource "aws_iam_policy" "schedule-policy" {
    name        = "c9-queenbees-terraform-schedule-policy"
    policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ecs:RunTask",
                    "states:StartExecution"
                ],
                "Resource": [
                    "${aws_ecs_task_definition.plant-pipeline-task-def.arn}",
                    "${aws_ecs_task_definition.rds-pipeline-task-def.arn}"
                ],
                "Condition": {
                    "ArnLike": {
                        "ecs:cluster": "${data.aws_ecs_cluster.c9-cluster.arn}"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": [
                    "*"
                ],
                "Condition": {
                    "StringLike": {
                        "iam:PassedToService": "ecs-tasks.amazonaws.com"
                    }
                }
            }
        ]
    })
}

# attach policy to schedule role
resource "aws_iam_policy_attachment" "schedule-policy-attachment" {
    name = "c9-queenbees-schedule-policy-attachment"
    roles = [aws_iam_role.schedule-role.name]
    policy_arn = aws_iam_policy.schedule-policy.arn
}

# create EventBridge schedule for plant pipeline
resource "aws_scheduler_schedule" "plant-pipeline-schedule" {
    name       = "c9-queenbees-plant-pipeline-schedule"
    schedule_expression = "cron(* * * * ? *)"
    flexible_time_window {
        mode = "OFF"
    }
    target {
        arn      = data.aws_ecs_cluster.c9-cluster.arn
        role_arn = aws_iam_role.schedule-role.arn
        ecs_parameters {
          task_definition_arn = aws_ecs_task_definition.plant-pipeline-task-def.arn
          task_count = 1
          launch_type = "FARGATE"
          platform_version = "LATEST"
          network_configuration {
            subnets = [ "subnet-0d0b16e76e68cf51b", "subnet-081c7c419697dec52", "subnet-02a00c7be52b00368" ]
            security_groups = [ "sg-020697b6514174b72" ]
            assign_public_ip = true
          }
        }
    }
}

# create EventBridge schedule for rds-s3 pipeline
resource "aws_scheduler_schedule" "rds-pipeline-schedule" {
    name       = "c9-queenbees-rds-s3-pipeline-schedule"
    schedule_expression = "cron(55 23 * * ? *)"
    flexible_time_window {
        mode = "OFF"
    }
    target {
        arn      = data.aws_ecs_cluster.c9-cluster.arn
        role_arn = aws_iam_role.schedule-role.arn
        ecs_parameters {
          task_definition_arn = aws_ecs_task_definition.rds-pipeline-task-def.arn
          task_count = 1
          launch_type = "FARGATE"
          platform_version = "LATEST"
          network_configuration {
            subnets = [ "subnet-0d0b16e76e68cf51b", "subnet-081c7c419697dec52", "subnet-02a00c7be52b00368" ]
            security_groups = [ "sg-020697b6514174b72" ]
            assign_public_ip = true
          }
        }
    }
}