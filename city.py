import urllib.request
import json
import xmljson
import lxml.etree

urlbase = "http://weather.livedoor.com/forecast/rss/primary_area.xml"
jsonurl = lxml.etree.parse(urlbase)
root = jsonurl.getroot()
path = "city_data.txt"

with open('conv.json', 'w') as fw:
    json.dump(xmljson.yahoo.data(root), fw, indent=2)

jsop = open("conv.json", "r")
jslo = json.load(jsop)


with open(path, mode="w") as f:
    
    for i in jslo["rss"]["channel"]["{http://weather.livedoor.com/%5C/ns/rss/2.0}source"]["pref"]:
        if type(i["city"]) == dict:
            f.write(i["city"]["title"]+":"+i["city"]["id"]+"\n")
        else:
            for j in i["city"]:
                f.write(j["title"]+":"+j["id"]+"\n")
