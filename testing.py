import pylas


lasJson = pylas.ConvertLasToJson("./las_files/las_with_lat_lon.las")
print([item for item in lasJson.WellInformationList if item.Mnemonic == "STAT"][0])
print(list(filter(lambda i: i.Mnemonic == "STAT", lasJson.WellInformationList))[0])
print("")
print(lasJson.WellInformationDict.STAT)

"""
import pymongo


client = pymongo.MongoClient()
warrior_db = client.Warrior
lasdataCollection = warrior_db.lasdata

l = lasdataCollection.find_one({}, {'Curves': False})
print(l['VersionInformation']['Wrap'])
"""
