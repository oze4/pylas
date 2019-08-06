import pymongo


client = pymongo.MongoClient()
warrior_db = client.Warrior
lasdataCollection = warrior_db.lasdata

l = lasdataCollection.find_one({}, {'Curves': False})
print(l['VersionInformation']['Wrap'])

