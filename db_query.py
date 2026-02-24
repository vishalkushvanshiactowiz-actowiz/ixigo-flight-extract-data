
# import mysql.connector
# import mysql.connecto
# import mysql-connector-python

import json

def json_to_dict(file_path):
    with open(file_path, "r") as file:
        dict_data = json.load(file)
    return dict_data

file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/ixigo flight/" +  "validate_data.json"
dict_data = json_to_dict(file_path)
# print(dict_data)
print(type(dict_data))


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

    # create new table
    # cursor.execute("CREATE TABLE flights ( id INT AUTO_INCREMENT PRIMARY KEY, Departure VARCHAR(10), Arrival VARCHAR(10), Date DATE, minimum_travel_price DECIMAL(10,2), maximum_travel_price DECIMAL(10,2), pictures_url TEXT ) ")
    # cursor.execute("CREATE TABLE fares ( id INT AUTO_INCREMENT PRIMARY KEY, flight_id INT, stops VARCHAR(20), fare DECIMAL(10,2), FOREIGN KEY (flight_id) REFERENCES flights(id) ) ")
    print("done ")
    # cursor.execute("SHOW Tables")
    # for db in cursor:
    #     print(db[0])

    # cursor.execute("SELECT * FROM flights")
    # for db in cursor:
    #     print(db[0])

    data = {
        "Departure": "DEL",
        "Arrival": "BOM",
        "Date": "March 02, 2026",
        "minimum_travel_price": 5000,
        "maximum_travel_price": 17308,
        "stop_wise_fare": [
            {"stops": "Non-Stop", "fare": 5000},
            {"stops": "1 Stop", "fare": 5501},
            {"stops": "2+ Stops", "fare": 0}
        ]
    }
    try:
        # 2. Insert Main Flight Data
        # Note: Ensure the date is in YYYY-MM-DD format for MySQL
        sql_flight = "INSERT INTO flights (departure, arrival, date, minimum_travel_price, maximum_travel_price) VALUES (%s, %s, %s, %s, %s)"
        flight_vals = (
        data['Departure'], data['Arrival'], '2026-03-02', data['minimum_travel_price'], data['maximum_travel_price'])
        cursor.execute(sql_flight, flight_vals)
        flight_id = cursor.lastrowid  # Get the ID of the inserted flight
        # 3. Insert Stop-wise Fares using executemany
        sql_fare = "INSERT INTO fares (flight_id, stops, fare) VALUES (%s, %s, %s)"
        # Add flight_id to each stop dictionary for foreign key mapping
        fare_data = []
        for item in data['stop_wise_fare']:
            fare_tuple = (flight_id, item['stops'], item['fare'])
            fare_data.append(fare_tuple)
        cursor.executemany(sql_fare, fare_data)


        # 4. Commit Changes
        connection.commit()
        print(f"Data stored successfully. Flight ID: {flight_id}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

except Exception as e:
    print(f"Error: {e}")

print("yes : now ")