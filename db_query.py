
import json
from datetime import datetime

def json_to_dict(file_path):
    with open(file_path, "r") as file:
        dict_data = json.load(file)
    return dict_data

file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/ixigo flight/" +  "validate_data.json"
data = json_to_dict(file_path)
# print(dict_data)
print(type(data))


import mysql.connector # Must include .connector

try:
    print("Connecting...")
    # Connection logic here
    connection = mysql.connector.connect(
        # host="3306",
        host="localhost",
        user="root",
        password="actowiz",
        port ="3306",
        database = "flight_db"

    )

    cursor = connection.cursor()

    # show all databases
    #  databases create .
    # cursor.execute("create database flight_db")
    # cursor.execute("SHOW DATABASES")
    # for db in cursor:
    #     print(db[0])

    # create new table  -- if table not exist then
    # cursor.execute("CREATE TABLE flights ( id INT AUTO_INCREMENT PRIMARY KEY, Departure VARCHAR(10), Arrival VARCHAR(10), Date DATE, minimum_travel_price DECIMAL(10,2), maximum_travel_price DECIMAL(10,2), airport_details JSON,  pictures_url TEXT ) ")
    # cursor.execute("CREATE TABLE fares ( id INT AUTO_INCREMENT PRIMARY KEY, flight_id INT, stops VARCHAR(20), fare DECIMAL(10,2), FOREIGN KEY (flight_id) REFERENCES flights(id) ) ")
    # cursor.execute("CREATE TABLE flight_options( id INT AUTO_INCREMENT PRIMARY KEY, parant_id INT, airline_name VARCHAR(100), flight_id VARCHAR(255), refundable VARCHAR(255), fare INT, stops INT, total_duration VARCHAR(20), start_timing VARCHAR(20), end_timing VARCHAR(20), baggage_info JSON, plane_change JSON, FOREIGN KEY (parant_id) REFERENCES flights(id) ) ")

    # show all table
    # cursor.execute("SHOW Tables")
    # for db in cursor:
    #     print(db[0])

    # cursor.execute("SELECT * FROM flights")
    # for db in cursor:
    #     print(db[0])

    # insert data in table
    parent_sql = """INSERT INTO flights 
                        (Departure, Arrival, Date, minimum_travel_price, maximum_travel_price, airport_details, pictures_url) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    raw_date = data["Date"]
    formatted_date = datetime.strptime(raw_date, "%B %d, %Y").date()
    parent_values = (
        data["Departure"],
        data["Arrival"],
        formatted_date,
        data["minimum_travel_price"],
        data["maximum_travel_price"],
        json.dumps(data["airport_details"]),  # Dictionary -> JSON String
        data["pictures_url "]
    )
    cursor.execute(parent_sql, parent_values)
    # 3. Get the ID of the row we just inserted
    last_search_id = cursor.lastrowid

    # insert data in child table
    child_sql = """INSERT INTO flight_options 
                       (parant_id, airline_name, flight_id, refundable, fare, stops, total_duration, start_timing, end_timing, baggage_info, plane_change) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"""

    for flight in data["flightDetails"]:
        child_values = (
            last_search_id,
            flight["airline_name"],
            flight["flight_id"],
            flight["refundable"],
            flight["fare"],
            flight["stops"],
            flight["total_duration"],
            flight["start_timing"],
            flight["end_timing"],
            json.dumps(flight["baggage"]) , # Nested baggage dict -> JSON String
            json.dumps(flight["plane_change"])  # Nested baggage dict -> JSON String
        )
        cursor.execute(child_sql, child_values)

    sql_fare = "INSERT INTO fares (flight_id, stops, fare) VALUES (%s, %s, %s)"
    # Add flight_id to each stop dictionary for foreign key mapping
    fare_data = []
    for item in data['stop_wise_fare']:
        fare_tuple = (last_search_id, item['stops'], item['fare'])
        fare_data.append(fare_tuple)
    cursor.executemany(sql_fare, fare_data)
    connection.commit()
    print(f"Success! Data saved under Search ID: {last_search_id}")

except Exception as e:
    print(f"Error: {e}")

print("yes : now ")