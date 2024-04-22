import json

def txt_to_json(txt_file):
    with open(txt_file, 'r') as f:
        data = f.readlines()
    
    # Extracting data from txt
    num_intersections = int(data[0].strip())
    intersections = []
    i = 1
    while i < len(data):
        intersection_id = int(data[i].strip())
        intersection_name = "Intersection_" + str(intersection_id)
        num_streets = int(data[i + 1].strip())
        streets = []
        for j in range(num_streets):
            street_data = data[i + 2 + j].strip().split()
            street_name = street_data[0]
            green_time = int(street_data[1])
            streets.append({"name": street_name, "green_time": green_time})
        intersections.append({"intersection_name": intersection_name, "streets": streets})
        i += num_streets + 2

    # Creating JSON structure
    json_data = {
        "number_of_intersections": num_intersections,
        "intersections": intersections
    }
    
    return json_data

def save_to_json(json_data, json_file):
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=3)

# Example usage
txt_file = "./solution_reporter/data/test1.json_V1_2.out.txt"
json_data = txt_to_json(txt_file)
save_to_json(json_data, "output.json")
