
# airline name headerTextWeb
# flightKeys flight id
# refundableType
# displayFare
# baggageDetails
# stops
# departureTime + departTime -- start time
# arrivalTime +  arrivalTime -- end time
# text -- total duration
# "origin": "DEL",
#                     "destination": "BOM",
#                     "date""

# departureAirport": "DEL",  start
#                                 "arrivalAirport  end

# minPrice
# maxPrice
# stopsFilter stop wise fare
# airportDetails
# bannerUrl



import json
from datetime import datetime

def json_to_dict(file_path):
    with open(file_path, "r") as file:
        dict_data = json.load(file)
    return dict_data

def extract_data(dict_data):
    ixigo_data = {}
    ixigo_data["Departure"] = dict_data.get("data").get("flightJourneys")[0].get("key")[0].get("origin")
    ixigo_data["Arrival"] = dict_data.get("data").get("flightJourneys")[0].get("key")[0].get("destination")
    flight_date = dict_data.get("data").get("flightJourneys")[0].get("key")[0].get("date")
    date_obj = datetime.strptime(flight_date, "%d%m%Y")
    ixigo_data["Date"] =  date_obj.strftime("%B %d, %Y")
    ixigo_data["minimum_travel_price"] =  dict_data.get("data").get("tripFilter").get("minPrice")
    ixigo_data["maximum_travel_price"] =  dict_data.get("data").get("tripFilter").get("maxPrice")

    ixigo_data["stop_wise_fare"] =  []
    stop_filter_list = dict_data.get("data").get("tripFilter").get("stopsFilter")
    for data in stop_filter_list:
        # print("val : ", data)
        ixigo_data["stop_wise_fare"].append({  "stops" : data["stopText"], "fare" : data["fare"] })

    ixigo_data["airport_details"] = {}
    airport_detail_dict = dict_data.get("data").get("airportDetails")
    for k in airport_detail_dict.keys():
        # print("key ", k)
        ixigo_data["airport_details"][k] = {}
        ixigo_data["airport_details"][k]["airport_name"] = airport_detail_dict[k]["airportName"]
        ixigo_data["airport_details"][k]["city"] = airport_detail_dict[k]["city"]
    ixigo_data["pictures_url "] = dict_data.get("data").get("bannerUrl")

    flight_fare_list = dict_data.get("data").get("flightJourneys")[0].get("flightFare")
    ixigo_data["flightDetails"] = []
    for data in flight_fare_list:
        single_flight = {}
        single_flight["airline_name"] = data.get("flightDetails")[0].get("headerTextWeb")
        single_flight["flight_id"] = data.get("flightKeys")
        single_flight["refundable"] = data.get("refundableType")
        single_flight["fare"] = data.get("fares")[0].get("fareDetails").get("displayFare")
        baggage_dict = {
            "checkInBaggage" : data.get("fares")[0].get("fareMetadata")[0].get("baggageDetails").get("checkInBaggage"),
            "handBaggage" : data.get("fares")[0].get("fareMetadata")[0].get("baggageDetails").get("handBaggage")
        }
        single_flight["baggage"] = baggage_dict
        single_flight["stops"] = data.get("flightFilter")[0].get("stops")
        start_time_word = data.get("flightFilter")[0].get("departTime")
        end_time_word = data.get("flightFilter")[0].get("arrivalTime")
        start_time_number = data.get("flightDetails")[0].get("departureTime")
        end_time_number = data.get("flightDetails")[0].get("arrivalTime")
        single_flight["start_timing"] = start_time_number + " " + start_time_word
        single_flight["end_timing"] = end_time_number + " " + end_time_word
        single_flight["total_duration"] = data.get("flightDetails")[0].get("duration").get("text")
        plane_change_list = data.get("flightDetails")[0].get("layover")
        if plane_change_list:
            location_name = data.get("flightDetails")[0].get("layover")[0].get("location")
            duration_time = data.get("flightDetails")[0].get("layover")[0].get("duration")
            plane_change_data  = { "location" : location_name, "duration" : duration_time }
        else:
            plane_change_data = {}
        single_flight["plane_change"] = plane_change_data
        ixigo_data["flightDetails"].append(single_flight)
    # print(ixigo_data)
    return ixigo_data

def dict_to_json(extract_data, file_path):
    with open(file_path, "w") as f:
        # f.write(json_data)
        json.dump(extract_data, f, indent=4)
    return f"Data vaidate successfully."

file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/ixigo flight/" +  "ixigo_flight.json"
dict_data = json_to_dict(file_path)
# print(dict_data)
print(type(dict_data))
extract_dict_data = extract_data(dict_data)
print(extract_dict_data)

destination_file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/ixigo flight/" + "validate_data.json"
result = dict_to_json(extract_dict_data, destination_file_path)
print(result)
