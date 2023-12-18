provider "aws" {
    region = "eu-west-2"
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