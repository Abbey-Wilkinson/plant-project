# Terraform
This folder is related to creating most of the AWS resources that we need through the use of Terraform.

## Assumptions
In order for the Terraform code to work, there are a few assumptions that need to be made:
- The first is that you should have an RDS instance using MicrosoftSQLServer set up and running.
- There are 3 ECR repositories made, each named:
    - *c9-queenbees-plant-pipeline-repo*: to store an image for the pipeline that extracts from the API and loads to the RDS.
    - *c9-queenbees-s3-pipeline-repo*: to store an image for the script that extracts from the RDS and loads to an S3.
    - *c9-queenbees-dashboard-repo*: to store an image that runs the dashboard.
- There is an ECS cluster that is available to run tasks and a service.

## Environment Variables
The code used environment variables. As a result, you will need to create a file called `credentials.auto.tfvars`. Within that file, you will need the following details:

`DB_HOST` : The host name or address of a database server.\
`DB_USER` : The user name to login to the database.\
`DB_PASSWORD` : The password to login to the database.\
`AWS_ACCESS_KEY_ID` : An access key id from AWS.\
`AWS_SECRET_ACCESS_KEY` : A secret key associated with the above identifier, serving as a password. 

## Files Explained
`main.tf` is the central configuration file. It describes the infrastructure resources you want to manage.

`variables.tf` is what is used to load the environment variables into the main file.

`.terraform.lock.hcl` is used by terraform to manage and lock the versions of the modules and providers required for the terraform configuration.

## How to run it
In order to run the terraform code, once you have the `credentials.auto.tfvars` file setup, then the following commands can be used:
1. `terraform init` : Initialises the whole thing.
2. `terraform plan` : Create an execution plan.
3. `terraform apply` : Allows you to execute your planned changes from the previous step.

And then finally, if you decide that if you want to stop the whole system, you can use:

4. `terraform destroy` : Destroys all resources defined previously.