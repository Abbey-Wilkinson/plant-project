provider "aws" {
    region = "eu-west-2"
}

data "aws_iam_role" "execution-role" {
    name = "ecsTaskExecutionRole"
}

# make ECR repositories for the images
resource "aws_ecr_repository" "plant_pipeline" {
  name = "c9-angelo-plant-pipeline-repo"
}

resource "aws_ecr_repository" "rds_pipeline" {
  name = "c9-angelo-rds-s3-pipeline-repo"
}

resource "aws_ecr_repository" "dashboard" {
  name = "c9-angelo-dashboard-repo"
}

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


# task definition for dashboard
# TODO: change the image string to the appropriate image in the ECR
# Also, configure the environment properly
resource "aws_ecs_task_definition" "dashboard-task-def" {
    family = "c9-angelo-dashboard-taskdef"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    container_definitions = jsonencode([
        {
            name: "dashboard"
            image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-angelo-dashboard-repo:dummy"
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