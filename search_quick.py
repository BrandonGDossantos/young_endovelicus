import json

from NutriDatabase import NDB


"""
    Query the database and list all standard references of an item
"""
def list_standard(ndb, item):
    res = NDB.list_standard(item)
    print(json.dumps(res, sort_keys=True, indent=4))

"""
    Query the database and list all branded references of an item
"""
def list_branded(ndb, item):
    res = NDB.list_branded(item)

"""
    Query the database for a specific ndbno
"""
def ndbno_lookup(ndb, ndbno):
    res = NDB.ndbno_lookup(ndbno)
    print(json.dumps(res, sort_keys=True, indent=4))

def compute_convert(name, eqv_in_g, value_in_g):
    # nutrient_map = {}
    # print("{} g".format(eqv_in_g))
    # print("{} g".format(value_in_g))
    eqv_to_oz = eqv_in_g * 0.0035
    normalized_oz = round((1/eqv_to_oz)/10, 2)
    normalized_value = round(float(value_in_g) * float(normalized_oz), 2)
    # print("{} oz: normalized eqv 1 oz".format(normalized_oz))
    print("\t {} units per oz".format(normalized_value))
    # nutrient_map[name] = normalized_value
    return normalized_value

def converter(ndb, item):
    nutrient_map = {}
    res = NDB.list_standard(item)
    # first = res['list']['item'][0]['ndbno']
    # res = NDB.ndbno_lookup(str(first))
    for item in res['list']['item']:
        print("[{}]: {}".format(item['offset'] + 1, item['name']))
    choice = input("Pick the item: ")
    res = NDB.ndbno_lookup(str(res['list']['item'][int(choice)-1]['ndbno']))
    counter = 1
    for measure in res['foods'][0]['food']['nutrients'][0]['measures']:
        print("[{}]: {} {}".format(counter, measure['qty'], measure['label']))
        counter += 1
        print('\n')
    choice = input("Choose your prefered measurement: ")
    for measurement in res['foods'][0]['food']['nutrients']:
        name = measurement['name']
        print("{}".format(name))
        # print(json.dumps(measurement['measures'][int(choice)-1], sort_keys=True, indent=4))
        nutrient_map[name] = compute_convert(name, measurement['measures'][int(choice)-1]['eqv'], measurement['measures'][int(choice)-1]['value'])
    return nutrient_map
    # print(json.dumps(ingredient_map, sort_keys=True, indent=4))


if __name__ == "__main__":
    api_key = "6I7oF4v5gemv0hZvOZH7pzFGRQzwLKGS5A4y3vWQ" 
    NDB = NDB(api_key)
    ingredient_map = {}
    yes = {'yes','y', 'ye' , ''}
    no = {'no','n'}
    x = True
    while x == True:
        item = input("Input Food: ")
        ingredient_map[item] = converter(NDB, str(item))    
        choice = input("Keep Going?: ").lower()
        if choice in yes:
            x = True
        elif choice in no:
            x = False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")
    print(json.dumps(ingredient_map, sort_keys=True, indent=4))

    # list_standard(NDB, "sliced bread")
    # list_branded(NDB, "715134255720")
    # ndbno_lookup(NDB, "09038")


