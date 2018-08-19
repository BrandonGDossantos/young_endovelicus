import json
import sys
from itertools import permutations
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
    Calculates the total ingredient oz 
"""


def calc_total(ingredient_map):
    pass
    total = {}
    for key, value in ingredient_map.items():

        total = {k: v + total[k] for k, v in value.items()}
    return total

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
    # iterate through dict(items) and output list of food objects
    for key, value in ingredient_map.items():
        item_obj = Item(key, value)
        item_objs.append(item_obj)
    return item_objs

"""
    Doubles ingredient macros
"""


def algorithm(ingredient_map):
    for key, value in ingredient_map.items():
        ingredient_map[key] = {k: v * 2 for k, v in value.items()}
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
    # nutrient_map['oz'] = 1
    return nutrient_map


"""
    Create permutation of multiples and objs
"""


def combine(item_objs):
    perm_multiples = permutate(len(item_objs))
    print(perm_multiples)

"""
    Permutate all number multiple combinations 
"""


def permutate(num_items):
    return list(permutations(range(1, num_items+1)))


def main():
    api_key = "6I7oF4v5gemv0hZvOZH7pzFGRQzwLKGS5A4y3vWQ"
    ndb_object = NDB(api_key)
    item_objs = ingredient_populator(ndb_object)
    item_combos = combine(item_objs)
    # print(json.dumps(ingredient_map, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
    # permutate(2)
