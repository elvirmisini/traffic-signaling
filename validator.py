import json

def load_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def validate_output(input_data, output_data):
    input_constraints = input_data.get("constraints", [])
    output_intersections = output_data.get("intersections", [])

    constraints_by_intersection = {}
    
    for constraint in input_constraints:
        if constraint["type"] == "simultaneously_signal":
            intersection_name = constraint["intersection_name"]
            constraints_by_intersection.setdefault(intersection_name, 0)
            constraints_by_intersection[intersection_name] += 1
    print(constraints_by_intersection)

    for intersection in output_intersections:
        intersection_name = intersection["intersection_name"]
        phases_count = len(intersection.get("phases", []))
        constraints_count = constraints_by_intersection.get(intersection_name, 0)
        if phases_count != constraints_count:
            return False

    return True

def main():
    input_file = "./input/instance_lakrishte_qerimi.json"
    output_file = "./output/instance_lakrishte_qerimi/instance_lakrishte_qerimi_144146_bvo.json"

    input_data = load_json_file(input_file)
    output_data = load_json_file(output_file)

    is_valid = validate_output(input_data, output_data)
    if is_valid:
        print("Output is valid.")
    else:
        print("Output is not valid.")

if __name__ == "__main__":
    main()
