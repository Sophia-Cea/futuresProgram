import json

def getJsonData(path):
    with open(path) as file:
        data = json.load(file)
    
    notifyAmntDay = data['notifyPriceDropDay']
    notifyAmntWeek = data['notifyPriceDropWeek']
    notifyAmntMonth = data['notifyPriceDropMonth']

    return notifyAmntDay, notifyAmntWeek, notifyAmntMonth