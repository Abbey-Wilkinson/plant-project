# Plants Project - Queen Bees 

## Cloud architecture
A high level overview of the cloud architecture can be seen below:

![cloud_architecture](images/plant-project-architecture.png)

There are two key pipelines here:

### API Pipeline
The first part is to extract data from the API then load it into a database for short term storage. The database in question will be a Microsoft SQL Server within an RDS. This pipeline will run as an ECS task that is triggered every minute using an EventBridge running on a schedule.

### Loading to long-term storage
The data from the RDS needs to be moved to a long-term storage solution, which in this case is a Redshift database. Redshift is chosen here are it is good for online analytical processing (OLAP) which will prove useful for the dashboard and will save on costs on the long run. Initially, an RDS may be more cost effective but considering that we want to run analytics, and as data accumulates, then eventually a Redshift will prove more cost effective.

The loading of the long-term database is conducted by a pipeline that is triggered every day by an EventBridge. The task triggered is an ECS task that reads from the RDS then uploads the contents to the Redshift. The data within the RDS is then reset.

The other key part of this project is dash-boarding. The dashboard here will be run using Streamlit and is hosted as an ECS service.