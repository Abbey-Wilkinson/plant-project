# RDS-S3 Pipeline

This folder contains all code and resources required to create a the pipeline which converts the database data into a csv and uploads it to a s3 bucket.

## Installation and Requirements

- It is recommended before stating any installations that you make a new virtual environment. 
- A new environment will be required for each folder in this repository.

- Install all requirements for this folder: `pip3 install -r requirements.txt`.

- Create a `.env` file with `touch .env`

## Assumptions
For this pipeline script to work, there are a few assumptions which need to be made:
- You have an RDS up and running with the correct data inside.
- You have an S3 bucket ready to upload csv files to.

- **Required env variables**: 
    - DB_HOST               -> arn to your AWS RDS.
    - DB_PORT               -> port the AWS RDS runs on. (e.g. If using T-SQL this typically uses 1433)
    - DB_USER               -> Your database username.
    - DB_NAME               -> Your database name.
    - DB_PASSWORD           -> Password to access your database.
    - AWS_ACCESS_KEY_ID     -> Your AWS access key ID to connect to AWS.
    - AWS_SECRET_ACCESS_KEY -> Your AWS secret access key to connect to AWS.

## Files 

- `requirements.txt` : This file contains all the required packages to run any other files
- `errors.py` : This file contains all the custom errors used in `daily_extract.py`. 
- `Dockerfile` : This file contains instructions to create a new docker image that runs `daily_extract.py`.
- `daily_extract.py` : This file contains the pipeline script .    
- `test_daily_extract.py`: This file contains the test for the pipeline script to make sure it's functional .

