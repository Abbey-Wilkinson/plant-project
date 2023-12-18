provider "aws" {
    region = "eu-west-2"
}

# make ECR repositories for the images
resource "aws_ecr_repository" "service" {
  name = "c9-angelo-plant-pipeline"
}