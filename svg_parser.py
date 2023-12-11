from svgelements import *
import requests
import json

# url for population total for specified year
# https://api.worldbank.org/v2/country/{id}/indicator/SP.POP.TOTL?date=2020&format=json

# url for GDP (US$) for specified year
# https://api.worldbank.org/v2/country/{id}/indicator/NY.GDP.MKTP.CD?date=2020&format=json

url = "https://api.worldbank.org/v2/country/"

#########################
# find locations that are identified in the svg file but not the API

sf = SVG.parse("./BlankMap-World.svg")
file = open('ids_not_in_API.txt', 'w')
count = 0
for element in sf:
    try:
        id = element.values['id']
        if len(id) == 2:
            response = requests.get(url + id + "?format=json")
            try:
                if response.json()[0]["message"][0]["key"] == 'Invalid value':
                    file.write(id + '\n')
            except: 
                count+=1
    except:
        pass
file.close()
print(count)
#########################




#########################
# collect all countries from API

response = requests.get(url + "?format=json")
i = 1
while i <= response.json()[0]["pages"]:
    print(i)
    url1 = url + "?page="+str(i) + "&format=json"
    resp = requests.get(url1)
    with open('00'+str(i)+'_data.json', 'w') as f:
        json.dump(resp.json(), f)
    i+=1
#########################




#########################
# find countries identified in the API but not the svg file

i = 1
iso2Codes = []
dict_iso2Codes = {}
while i <= 6:
    f = open('00' + str(i) + '_data.json')
    data = json.load(f)
    for j in data[1]:
        iso2Codes.append(j["iso2Code"])
        dict_iso2Codes[j["iso2Code"]] = j["name"]
    i+=1

sf = SVG.parse("./BlankMap-World.svg")
file = open('iso2Codes_not_in_svg.txt', 'w')
id_Array = []
for element in sf:
    try:
        id = element.values['id']
        if len(id) == 2:
            id_Array.append(id)
    except:
        pass

for x in iso2Codes:
    xLower = str(x).lower()
    if xLower not in id_Array:
        file.write(x + ' : ' + dict_iso2Codes[x] + '\n')
file.close()
#########################




#########################
# test individual iso2Codes
# sf = SVG.parse("./BlankMap-World.svg")

# for element in sf:
#     try:
#         id = element.values['id']
#         if id == 'xk':
#             response = requests.get(url + id + "?format=json")
#             print(response.json())
#     except:
#         pass