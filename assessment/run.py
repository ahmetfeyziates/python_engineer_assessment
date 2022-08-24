from collections import defaultdict
import json
from tokenize import cookie_re
import pandas as pd
import sqlalchemy
from flask import Flask


app = Flask(__name__)
app.json.sort_keys = False


# Function to apply two types of basic data cleaning.
def clean(data):
    for index, person in enumerate(data):
        person["Interest1"] = person["Interest1"].strip().lower()
        person["Interest2"] = person["Interest2"].strip().lower()
        person["Interest3"] = person["Interest3"].strip().lower()
        person["Interest4"] = person["Interest4"].strip().lower()


# Function to remove people without any interests.
def filter_out_boring_people(data):
    for index, person in enumerate(data):
        if person["Interest1"] == "" and \
            person["Interest2"] == "" and \
            person["Interest3"] == "" and \
            person["Interest4"] == "":

            del data[index]


# Function to store the unprocessed (dirty) csv file to the database.
def store_csv_into_db(file_path):
    # connect to the database
    engine = sqlalchemy.create_engine("mysql://datatest:alligator@database/datatestdb")
    connection = engine.connect()    
    metadata = sqlalchemy.schema.MetaData(engine)  

    # make an ORM object to refer to the table
    Person = sqlalchemy.schema.Table('person', metadata, autoload=True, autoload_with=engine)

    # clean out table from previous runs
    connection.execute(Person.delete())    

    df = pd.read_csv(file_path, keep_default_na=False)
    # Rename df columns to align with database columns
    df.rename(columns={
                        "Name": "name", 
                        "Age": "age", 
                        "City": "city", 
                        "Interest1": "interest1", 
                        "Interest2": "interest2",
                        "Interest3": "interest3",
                        "Interest4": "interest4",
                        "PhoneNumber": "phone_number"
                      },
                      inplace=True
             )

    for index, row in df.iterrows():
        print (".")
        connection.execute(Person.insert(),**row)
    
    rows = connection.execute(sqlalchemy.sql.select([Person])).fetchall()
    print("Found rows in database: ", len(rows))     


@app.route("/stats/", methods=['GET'])
def return_stats(db_uri=None):
    # connect to the database (use hostname based uri if called via endpoint)
    if not db_uri:
        db_uri = "mysql://datatest:alligator@127.0.0.1/datatestdb"

    engine = sqlalchemy.create_engine(db_uri)
    connection = engine.connect()    
    metadata = sqlalchemy.schema.MetaData(engine)  

    # make an ORM object to refer to the table
    Person = sqlalchemy.schema.Table('person', metadata, autoload=True, autoload_with=engine)

    interests_map = defaultdict(lambda: 0)
    
    statresults = connection.execute(sqlalchemy.sql.select([
                                    sqlalchemy.sql.func.min(Person.c.age).label('min_age'), 
                                    sqlalchemy.sql.func.max(Person.c.age).label('max_age'),
                                    sqlalchemy.sql.func.avg(Person.c.age).label('avg_age')
                                ])).fetchone()

    city_result = connection.execute(sqlalchemy.sql.select([
                                    sqlalchemy.sql.func.count().label('count'), 
                                    Person.c.city
                                ]).group_by(Person.c.city) \
                                .order_by(sqlalchemy.sql.desc('count')) \
                                .limit(1)) \
                                .fetchone()

    rows = connection.execute(sqlalchemy.sql.select([Person])).fetchall()
    for row in rows:
        interests_map[row["interest1"]] += 1
        interests_map[row["interest2"]] += 1
        interests_map[row["interest3"]] += 1
        interests_map[row["interest4"]] += 1
    connection.close()  
    sorted_interests_map = sorted(interests_map.items(), key=lambda x: x[1], reverse=True)
    common_interests = [tup[0] for tup in sorted_interests_map]
    top_five_most_common_interests = common_interests[:5]

    response = dict()
    response["min_age"] = statresults["min_age"]
    response["max_age"] = statresults["max_age"]
    response["avg_age"] = statresults["avg_age"]
    response["city_with_most_people"] = city_result["city"]
    response["top_five_most_common_interests"] = top_five_most_common_interests
    return (response)


def run():
    print("Hello, Profasee!")    

    # Do some cleaning on the json form of the data as per assessment requirements.
    with open('../data/people.json', 'r') as f:
        data = json.load(f)
    
        print ("length of dataset before filtering, and cleanings: ", len(data))
        # Remove people who have no interests.
        filter_out_boring_people(data)
        # Do some cleaning on data according to assessment requirements.
        # 1. Standardize the capitalization of the interests.
        # 2. Delete the interests where the data is missing.
        clean(data)
        print ("length of dataset after filtering, and cleanings: ", len(data))

    # Store the csv file (uncleaned) into the database. 
    # Uncomment and run the following line only once after container re-creation.
    #store_csv_into_db('../data/people.csv')

    # Get some statistics from the database.
    my_response = return_stats(db_uri="mysql://datatest:alligator@database/datatestdb")
    print(my_response)


if __name__ == "__main__":
    run()
