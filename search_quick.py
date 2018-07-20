import json
from NutriDatabase import NDB


"""
	Query the database and list all standard references of an item
"""
def list_standard(ndb, item):
	res = NDB.list_standard(item)
	print(json.dumps(res, sort_keys=True, indent=4))

"""
	Query the database and list all standard references of an item
"""
def list_branded(ndb, item):
	res = NDB.list_branded(item)
	print(json.dumps(res, sort_keys=True, indent=4))




if __name__ == "__main__":
    api_key = "6I7oF4v5gemv0hZvOZH7pzFGRQzwLKGS5A4y3vWQ" 
    NDB = NDB(api_key)
    # list_standard(NDB, "butter")
    list_branded(NDB, "butter")

