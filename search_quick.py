import json
from NutriDatabase import NDB

def list_standard(ndb, item):
	res = NDB.list_standard(item)
	print(json.dumps(res, sort_keys=True, indent=4))
	# res = grey.get_context(ip.decode("utf-8"))
	# print(res)

def ndbno_lookup(ndb, ndbno):
    res = NDB.ndbno_lookup(ndbno)
    print(json.dumps(res, sort_keys=True, indent=4))

if __name__ == "__main__":
    api_key = "6I7oF4v5gemv0hZvOZH7pzFGRQzwLKGS5A4y3vWQ" 
    NDB = NDB(api_key)
    list_standard(NDB, "brown rice")
    ndbno_lookup(NDB, "09039")
