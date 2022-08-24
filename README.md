# Code test for python engineers

## Purpose

This is a test to demonstrate your understanding of data integrations, SQL databases, and ability to manipulate data into a format that is accessible for data scientists.

## Prerequisites

- Knowledge of python and the tools to integrate with APIs, process data, and interact with a file system and a SQL database.
- Knowledge of relational databases, including how to create tables, insert data, and query data. For the purpose of this test, we are using MySQL.
- Familiarity with Docker for container management, which we use through the Docker Compose tool. You will need Docker and Docker Compose installed on your development machine.
- Familiarity with Git for source control, and a github.com account which will be used for sharing your code.

We have included a test script that will ensure that the file system and MySQL database are set up correctly and accessible.

## Background

We have provided a Github repo containing:

- A **docker compose.yml** file that configures a container for the MySQL database and the script
- A **Dockerfile** to build and run the python script
- A **mysql-schemas** folder containing a test.sql file. You can add your sql schemas here.

## Test

To ensure the database is up and running, the following test can be run:

```
docker-compose up --build test
```

You should see output similar to the following:

```
Attaching to ml_data_engineer_assessment_test_1
test_1        | wait-for-it.sh: waiting 15 seconds for database:3306
test_1        | wait-for-it.sh: database:3306 is available after 0 seconds
test_1        | Found rows in database:  4
test_1        | Test Successful
ml_data_engineer_assessment_test_1 exited with code 0
```

## Assessment

The assessment consists of a series of small tasks to demonstrate your ability to perform the role of a python engineer at Profasee. We will be looking for both your ability to complete the tasks as well as the tools, data structures, python features, and code structure you use to accomplish the final result. Any python package needed can be added to the requirements.txt file. All code should be added to the `assessments` folder and be able to be run with the following command:
```
docker-compose up --build assessment
```

Fork the git repo to your own Github account and complete the following tasks:

1. Download the CSV hosted at https://profasee-data-engineer-assessment-api.onrender.com/people.csv:
* Store the raw data in the `/data` directory.
* Convert the CSV to JSON format and store in the `/data` directory.
2. Inspect the data and list ways that the data can be cleaned up before being stored for a data science team to use.

**Following types of cleanings can be applied to the downloaded data.**

**1. Standardize the capitalization of the interests.**

**2. Leading and trailing spaces should be eliminated from the strings representing interests.**

**3. Phone Number should be normalized into standart international canonical form, without any character in between** 

**4. Delete the interests where the data is missing.**

* Write code to peform at least two types of the cleaning.

**Proper functions have been written to apply the first two cleanings on the data.**

* Write unit tests to show the data cleaning functions work as expected.

**Unit tests have been written using pytest, and stored under directory named "tests".**
**Unit tests can be run via issuing the following commands from terminal:**

    % cd tests

    % pytest

* Write a function to filter people who have no interests.

**Function named "filter_out_boring_people" have been written for this purpose.**

3. Design a database schema to hold the data for the people in the CSV.
* Store the schema file in the `mysql-schemas` directory. These will be applied when the database container is created.

**Designed Database table has been defined in mysql-schemas/test.sql**

* Write code to load the data from the CSV into the database.

**Function named "store_csv_into_db" reads the csv and stores the data there in without any cleaning.**

**This function should be called once after container creation**

4. Create a function that uses the database tables to return the following stats of the people data:
* The minimum, maximum, and average age
* The city with the most people
* The top 5 most common interests

**Funation named "return_stats()" returns the above requested statistics.**

5. Create an API that serves an endpoint to return the data in Task 4.

**The function created at step 4 above have been specified as the API endpoint via Flask Framework.**
**The endpoint can be launched with:**

    % cd assessments
    % flask --debug --app=run.py run

And the endpint can be reached by issuing following GET request towards the declared endpoint:

    http://localhost:5000/stats/

Share a link to the cloned github repo with the completed tasks so we can review your code ahead of your interview.
