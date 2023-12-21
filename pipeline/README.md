# API Pipeline Script

This folder should contain all code and resources required to run the pipeline that connects to the [API found here](https://data-eng-plants-api.herokuapp.com/plants/8). The last digit determines the ID of the plants.
The files in this folder are used to connect to the API, extract and clean the plant information, then load it into the database.

## Installation and Requirements

- It is recommended before stating any installations that you make a new virtual environment. 
- A new environment will be required for each folder in this repository.

- Install all requirements for this folder: `pip3 install -r requirements.txt`.

- Create a `.env` file with `touch .env`

- **Required env variables**: 
    - DB_HOST               -> Arn to your AWS RDS
    - DB_PORT               -> Port the AWS RDS runs on. (e.g. If using T-SQL this typically uses 1433)
    - DB_USER               -> Your database username.
    - DB_NAME               -> Your database name.
    - DB_PASSWORD           -> Password to access your database.

## Files 

- `requirements.txt` : This file contains all the required packages to run any other files
- `Dockerfile` : This file contains instructions to create a new docker image that runs `pipeline.py`.
This is ran every minute on AWS
- `schema.sql` : This .sql file can be ran to create all of your tables needed for your pipeline - and can be ran by using the line:
sqlcmd -S DB_HOST,DB_PORT -U DB_USER -P DB_PASSWORD -i PATH_TO_SCHEMA_FROM_CURRENT_REPO if you have a database called `plants`
- `pipeline.py` : Imports functions from the below and completes the entire process of extracting, cleaning and loading.    
  - `extract.py` : Extracts data from the API - typically the longest part of the process.
  - `transform.py` : Cleans the data, making it usable to create visualisations and gain information.
  - `load.py` : Loads the data into the database.
  - `errors.py` : Custom errors are contained in here, used for when something goes wrong in the pipeline. 

