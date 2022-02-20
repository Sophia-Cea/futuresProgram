import json

def getJsonData(path):
    with open(path) as file:
        data = json.load(file)

    return data

def getNotifData(data):
    notifyAmntDay = data['notifyPriceDropDay']
    notifyAmntWeek = data['notifyPriceDropWeek']
    notifyAmntMonth = data['notifyPriceDropMonth']

    return notifyAmntDay, notifyAmntWeek, notifyAmntMonth

def getTimerData(data):
    refreshRate = data['refreshFrq']
    notifRate = data['notifFrq']
    return refreshRate, notifRate


def writeSettings(path, day, week, month, refresh, notif):
    data = {
        "notifyPriceDropDay": day,
        "notifyPriceDropWeek": week,
        "notifyPriceDropMonth": month,
        "notifFrq": notif,
        "refreshFrq": refresh
    }
    with open(path, 'w') as f:
        json.dump(data, f)
