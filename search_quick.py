from NutriDatabase import NDB

def sr_quick(ndb, item):
	res = NDB.standard_quick(item)
	print(res)
	# res = grey.get_context(ip.decode("utf-8"))
	# print(res)

if __name__ == "__main__":
    api_key = "6I7oF4v5gemv0hZvOZH7pzFGRQzwLKGS5A4y3vWQ" 
    NDB = NDB(api_key)
    item = "butter"
    sr_quick(NDB, item)