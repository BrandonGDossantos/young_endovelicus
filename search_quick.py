import argparse
import json
import copy
import sys
import itertools
import pickle
from NutriDatabase import NDB

class Item(object):
    """docstring for Item"""
    def __init__(self, name, map_ingredients):
        self.name = name
        self.carb = map_ingredients['Carbohydrate, by difference']
        self.calories = map_ingredients['Energy']
        self.fat = map_ingredients['Total lipid (fat)']
        self.protein = map_ingredients['Protein']
        self.oz = 1

"""
    Query the database and list all standard references of an item
"""


def list_standard(ndb_object, item):
    res = ndb_object.list_standard(item)
    print(json.dumps(res, sort_keys=True, indent=4))

"""
    Query the database for a specific ndbno
"""


def ndbno_lookup(ndb_object, ndbno):
    res = ndb_object.ndbno_lookup(ndbno)
    print(json.dumps(res, sort_keys=True, indent=4))

"""
    Compute the total of nutrients given a dictionary of ingredients
"""
def compute_total(ingredient_map):
    total = {}
    for key, value in ingredient_map.items():
        for k, v in value.items():
            if k not in total:
                total[k] = round(v, 2)
            else: 
                total[k] += round(v, 2)
    return total

"""
    Compare the combo recipe with macros
"""
def compare(recipe_map, arg_dict):
    points = 0
    if 'Proteins' in arg_dict.keys():
        points += abs(recipe_map['total']['Protein'] - arg_dict['Proteins'])
    if 'Carbs' in arg_dict.keys():
        points += abs(recipe_map['total']['Carbohydrate, by difference'] - arg_dict['Carbs'])
    if 'Fats' in arg_dict.keys():
        points += abs(recipe_map['total']['Total lipid (fat)'] - arg_dict['Fats'])
    if 'Calories' in arg_dict.keys():
        points += abs(recipe_map['total']['Energy'] - arg_dict['Calories'])
    # print("Points: {}".format(points))
    with open("tmp", "a") as file:
        for key, val in recipe_map.items():
            # print("{} : {}".format(key, recipe_map[key]['oz']))
            file.write("Points: {}\n".format(points))
            file.write("{} : {}\n".format(key, recipe_map[key]['oz']))


"""
    Multiply each nurtient by combo
"""
def multiplier(ingredient_map, arg_dict):
    # Produce a list of possible combinations
    prod_oz = list(itertools.product([1,2,3,4,5,6,7,8,9,10], repeat=len(ingredient_map)))
    # Assign combo 'oz' values to each ingredient 
    for combo in prod_oz:
        template = copy.deepcopy(ingredient_map)
        i = 0
        for key, val in template.items():
               for vkey in val:
                    val[vkey] *= combo[i]   
               i += 1
        template['total'] = compute_total(template)
        compare(template, arg_dict)

        # print(json.dumps(template, sort_keys=True, indent=4))

"""
    Loop through inputed ingredients and commense conversion to oz
"""


def ingredient_populator(ndb_object):
    item_objs = []
    ingredient_map = {}
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}
    x = True
    while x == True:
        item = input("Input Food: ")
        ingredient_map[item] = converter(ndb_object, str(item))
        choice = input("Keep Going?: ").lower()
        if choice in yes:
            x = True
        elif choice in no:
            x = False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")
    # Call compute_total() to populate the total key
    # ingredient_map['total'] = compute_total(ingredient_map)
    # print(json.dumps(ingredient_map, sort_keys=True, indent=4))
    return ingredient_map 


"""
    Normalizes
"""


def compute_convert(name, eqv_in_g, value_in_g):
    eqv_to_oz = eqv_in_g * 0.0035
    normalized_oz = round((1 / eqv_to_oz) / 10, 2)
    normalized_value = round(float(value_in_g) * float(normalized_oz), 2)
    return normalized_value

"""
    Menus to pick item and measurement before conversion
"""


def converter(ndb_object, item):
    nutrient_map = {}
    res = ndb_object.list_standard(item)
    for item in res['list']['item']:
        print("[{}]: {}".format(item['offset'] + 1, item['name']))
    choice = input("Pick the item: ")
    res = ndb_object.ndbno_lookup(
        str(res['list']['item'][int(choice) - 1]['ndbno']))
    counter = 1
    for measure in res['foods'][0]['food']['nutrients'][0]['measures']:
        print("[{}]: {} {}".format(counter, measure['qty'], measure['label']))
        counter += 1
    choice = input("Choose your prefered measurement: ")
    for measurement in res['foods'][0]['food']['nutrients']:
        name = measurement['name']
        nutrient_map[name] = compute_convert(name, measurement['measures'][int(
            choice) - 1]['eqv'], measurement['measures'][int(choice) - 1]['value'])
    nutrient_map['oz'] = 1

    return nutrient_map


if __name__ == "__main__":
    api_key = "6I7oF4v5gemv0hZvOZH7pzFGRQzwLKGS5A4y3vWQ" 
    arg_dict = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("-Proteins", type=float, help="Proteins")
    parser.add_argument("-Carbs", type=float, help="Carbohydrates")
    parser.add_argument("-Fats", type=float, help="Fats")
    parser.add_argument("-Calories", type=float, help="Calories")
    args = parser.parse_args()
    for arg in vars(args):
        arg_dict[arg] = getattr(args, arg)
    ndb_object = NDB(api_key)
    ingredient_map = ingredient_populator(ndb_object)
    
   # with open("test_recipe", "wb") as f:
   #     f.write(pickle.dumps(ingredient_map))
   #     f.close()
   ## file = open("test_recipe", "rb")
   # ingredient_map = pickle.load(file)
   # file.close()
    multiplier(ingredient_map, arg_dict)
    #print(json.dumps(ingredient_map, sort_keys=True, indent=4))
