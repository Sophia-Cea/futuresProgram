import json

def getJsonData(path):
    with open(path) as file:
        data = json.load(file)
    
    notifyAmnt = data['notifyPriceDrop']

    return notifyAmnt