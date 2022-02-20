# import queue
import tkinter
from tkinter import filedialog
tkinter.Tk().withdraw()
import pygame
from utils import *
import pygame.display
from random import randint
from scraper import *
from getNotifSettings import *
import pox
from notify import *

# TODO: implement a few cleanup functions
# add a page that lists all the futures that were notified about
# improve settings.json so it writes default settings to it if its empty
# change settings.json to a better name
# have a thingy check if something was already notified about in the day
# or if it dropped any more since last refresh


# currently doing: optimizing and adding idle state


# Functions for screens~~~~~~~
def changeStateToFullList():
    Screen.state = 1

def changeStateToMenu():
    Screen.state = 0

def changeStateToFutureView():
    Screen.state = 2

def changeStateToNotif():
    Screen.state = 3

def setIdle():
    global screen
    screen = pygame.display.set_mode([1,1], pygame.HIDDEN)
    Screen.state = 4
    Screen.idling = True

def stopIdling():
    global screen
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
    Screen.state = 0
    Screen.idling = False

def writeSettingsAndMenuState():
    writeSettings(path, notifyAmntDay, notifyAmntWeek, notifyAmntMonth, refreshRate, notifRate)
    Screen.state = 0

def setupFutureView(name):
    global stockBeingViewed
    stockBeingViewed = name
    for unit in dayInfo:
        if unit['label'] == name:
            dayDict = unit
    for unit in weekInfo:
        if unit['label'] == name:
            weekDict = unit
    for unit in monthInfo:
        if unit['label'] == name:
            monthDict = unit
    futureView.texts[0]= Text(name, 'title', Colors.textCol, (50,5), True)
    futureView.texts[1] = Text('Day: ' + str(dayDict['perf']) + '%', 'subtitle', Colors.textCol, (50, 20), True)
    futureView.texts[2] = Text('Week: ' + str(weekDict['perf']) + '%', 'subtitle', Colors.textCol, (50, 25), True)
    futureView.texts[3] = Text('Month: ' + str(monthDict['perf']) + '%', 'subtitle', Colors.textCol, (50, 30), True)
    if muteList[name] == False:
        futureView.buttons[1] = Button('Mute', Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(43, 50, 14, 6), 20, muteStock)
    if muteList[name] == True:
        futureView.buttons[1] = Button('Unmute', Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(43, 50, 14, 6), 20, unMuteStock)

def addBiggestDroppersToMenu():
    for i in range(5):
        text = Text(str(dayInfo[len(dayInfo)-i-1]['label']) + ": " + str(dayInfo[len(dayInfo)-i-1]['perf']) + '%', 'button', Colors.textCol, (30, 75 + i*4), True)
        menu.texts.append(text)
        text = Text(str(dayInfo[len(weekInfo)-i-1]['label']) + ": " + str(weekInfo[len(weekInfo)-i-1]['perf']) + '%', 'button', Colors.textCol, (70, 75 + i*4), True)
        menu.texts.append(text)

def writeFullListDay():
    fullListDay = []
    for i in range(int(len(dayInfo)/3)):
        text = Text(dayInfo[i]['label'], 'paragraph', Colors.textCol, (25, 22 + i*4), True)
        fullListDay.append(text)

    for i in range(int(len(dayInfo)/3)):
        text = Text(dayInfo[int(len(dayInfo)/3)+i]['label'], 'paragraph', Colors.textCol, (50, 22 + i*4), True)
        fullListDay.append(text)

    for i in range(int(len(dayInfo)/3)):
        text = Text(dayInfo[int(len(dayInfo)*2/3)+i]['label'], 'paragraph', Colors.textCol, (75, 22 + i*4), True)
        fullListDay.append(text)

    for text in fullListDay:
        fullList.texts.append(text)

def writeFullListWeek():
    fullListWeek = []
    for i in range(int(len(weekInfo)/3)):
        text = Text(weekInfo[i]['label'], 'paragraph', Colors.textCol, (25, 22 + i*4), True)
        fullListWeek.append(text)
    
    for i in range(int(len(weekInfo)/3)):
        text = Text(weekInfo[int(len(weekInfo)/3)+i]['label'], 'paragraph', Colors.textCol, (50, 22 + i*4), True)
        fullListWeek.append(text)

    for i in range(int(len(weekInfo)/3)):
        text = Text(weekInfo[int(len(weekInfo)*2/3)+i]['label'], 'paragraph', Colors.textCol, (75, 22 + i*4), True)
        fullListWeek.append(text)

    for text in fullListWeek:
        fullList.texts.append(text)

def writeFullListMonth():
    fullListMonth = []
    for i in range(int(len(monthInfo)/3)):
        text = Text(monthInfo[i]['label'], 'paragraph', Colors.textCol, (25, 22 + i*4), True)
        fullListMonth.append(text)

    for i in range(int(len(monthInfo)/3)):
        text = Text(monthInfo[int(len(dayInfo)/3)+i]['label'], 'paragraph', Colors.textCol, (50, 22 + i*4), True)
        fullListMonth.append(text)

    for i in range(int(len(monthInfo)/3)):
        text = Text(monthInfo[int(len(dayInfo)*2/3)+i]['label'], 'paragraph', Colors.textCol, (75, 22 + i*4), True)
        fullListMonth.append(text)

    for text in fullListMonth:
        fullList.texts.append(text)

def resetFullList():
    fullList.texts = fullList.texts[:1]

def setFullListDay():
    resetFullList()
    writeFullListDay()

def setFullListWeek():
    resetFullList()
    writeFullListWeek()

def setFullListMonth():
    resetFullList()
    writeFullListMonth()

def fullListUpdate():
    pos = pygame.mouse.get_pos()
    for button in fullList.buttons:
        if button.checkMouseOver(pos):
            button.hovering = True
        else:
            button.hovering = False
    for text in fullList.texts:
        if text.checkMouseOver() and text != fullList.texts[0]:
            pygame.draw.rect(screen, Colors.accentCol, text.rect, 3, 0)

def fullListInput(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in fullList.buttons:
                if button.checkMouseOver(pos):
                    if button.onClickFunc != None:
                        button.onClickFunc()
            i = 0
            for text in fullList.texts:
                if text.checkMouseOver():
                    setupFutureView(text.content)
                    changeStateToFutureView()
                i += 1

def pickNewFilePath():
    try:
        path = filedialog.askopenfilename()
    except:
        print("couldnt open file dialog")
    return path

def getSettingsPath():
    try:
        path = pox.find('settings.json')[0]
    except:
        path = pickNewFilePath()
    return path

def setEditing1():
    global editing1, editing2, editing3, editing4, editing5, notifyAmntDay
    if editing1:
        editing1 = False
        if len(notifyAmntDay) == 0:
            notifyAmntDay = "None"
            notifSettings.texts[2] = Text(str(notifyAmntDay), 'subtitle', Colors.textCol, (3, 30), False)
    else:
        editing1 = True
        editing2 = False
        editing3 = False
        editing4 = False
        editing5 = False
        if notifyAmntDay == "None":
            notifyAmntDay = ""

def setEditing2():
    global editing1, editing2, editing3, editing4, editing5, notifyAmntWeek
    if editing2:
        editing2 = False
        if len(notifyAmntWeek) == 0:
            notifyAmntWeek = "None"
            notifSettings.texts[3] = Text(str(notifyAmntWeek), 'subtitle', Colors.textCol, (3, 30), False)
    else:
        editing1 = False
        editing2 = True
        editing3 = False
        editing4 = False
        editing5 = False
        if notifyAmntWeek == "None":
            notifyAmntWeek = ""

def setEditing3():
    global editing1, editing2, editing3, editing4, editing5, notifyAmntMonth
    if editing3:
        editing3 = False
        if len(notifyAmntMonth) == 0:
            notifyAmntMonth = "None"
            notifSettings.texts[4] = Text(str(notifyAmntMonth), 'subtitle', Colors.textCol, (3, 30), False)
    else:
        editing1 = False
        editing2 = False
        editing3 = True
        editing4 = False
        editing5 = False
        if notifyAmntMonth == "None":
            notifyAmntMonth = ""

def setEditing4():
    global editing1, editing2, editing3, editing4, editing5, refreshRate
    if editing4:
        editing4 = False
        if len(refreshRate) == 0:
            refreshRate = "None"
            notifSettings.texts[7] = Text(str(refreshRate), 'subtitle', Colors.textCol, (3, 60), False)
    else:
        editing1 = False
        editing2 = False
        editing3 = False
        editing4 = True
        editing5 = False
        if refreshRate == "None":
            refreshRate = ""

def setEditing5():
    global editing1, editing2, editing3, editing4, editing5, notifRate
    if editing5:
        editing5 = False
        if len(notifRate) == 0:
            notifRate = "None"
            notifSettings.texts[8] = Text(str(notifRate), 'subtitle', Colors.textCol, (3, 60), False)
    else:
        editing1 = False
        editing2 = False
        editing3 = False
        editing4 = False
        editing5 = True
        if notifRate == "None":
            notifRate = ""

def notifSettingsRender(screen):
    screen.blit(pygame.transform.scale(notifSettings.bg, screen.get_size()), (0,0))
    for button in notifSettings.buttons:
        button.draw(screen)
    for text in notifSettings.texts:
        text.draw(screen)
    if editing1:
        pygame.draw.line(screen, Colors.accentCol, (screen.get_width()/100*3, screen.get_height()/100*35), (screen.get_width()/100*30, screen.get_height()/100*35), 5)
    if editing2:
        pygame.draw.line(screen, Colors.accentCol, (screen.get_width()/100*3, screen.get_height()/100*50), (screen.get_width()/100*30, screen.get_height()/100*50), 5)
    if editing3:
        pygame.draw.line(screen, Colors.accentCol, (screen.get_width()/100*3, screen.get_height()/100*65), (screen.get_width()/100*30, screen.get_height()/100*65), 5)
    if editing4:
        pygame.draw.line(screen, Colors.accentCol, (screen.get_width()/100*50, screen.get_height()/100*42), (screen.get_width()/100*70, screen.get_height()/100*42), 5)
    if editing5:
        pygame.draw.line(screen, Colors.accentCol, (screen.get_width()/100*50, screen.get_height()/100*67), (screen.get_width()/100*70, screen.get_height()/100*67), 5)

def notifSettingsUpdate():
    pos = pygame.mouse.get_pos()
    for button in notifSettings.buttons:
        if button.checkMouseOver(pos):
            button.hovering = True
        else:
            button.hovering = False
    if editing1:
        notifSettings.texts[2] = Text(str(notifyAmntDay) + "% in a day", 'paragraph', Colors.textCol, (3, 30), False)
    if editing2:
        notifSettings.texts[3] = Text(str(notifyAmntWeek) + "% in a week", 'paragraph', Colors.textCol, (3, 45), False)
    if editing3:
        notifSettings.texts[4] = Text(str(notifyAmntMonth) + "% in a month", 'paragraph', Colors.textCol, (3, 60), False)
    if editing4:
        notifSettings.texts[7] = Text("Every " + str(refreshRate) + " minutes", 'paragraph', Colors.textCol, (60, 38), True)
    if editing5:
        notifSettings.texts[8] = Text("Every " + str(notifRate) + " minutes", 'paragraph', Colors.textCol, (60, 63), True)

def notifSettingsInput(events):
    global notifyAmntDay, notifyAmntMonth, notifyAmntWeek, refreshRate, notifRate, editing1, editing2, editing3, editing4, editing5
    for event in events:
        if event.type == pygame.KEYDOWN:
            if editing1:
                if event.key == pygame.K_BACKSPACE:
                    if len(notifyAmntDay) > 0:
                        notifyAmntDay = notifyAmntDay[:-1]
                elif event.key == pygame.K_RETURN:
                    editing1 = False
                    if len(notifyAmntDay) == 0:
                        notifyAmntDay = "None"
                        notifSettings.texts[2] = Text(str(notifyAmntDay), 'subtitle', Colors.textCol, (3, 30), False)
                elif checkNum(event.unicode):
                    notifyAmntDay += event.unicode
            if editing2:
                if event.key == pygame.K_BACKSPACE:
                    if len(notifyAmntWeek) > 0:
                        notifyAmntWeek = notifyAmntWeek[:-1]
                elif event.key == pygame.K_RETURN:
                    editing2 = False
                    if len(notifyAmntWeek) == 0:
                        notifyAmntWeek = "None"
                        notifSettings.texts[3] = Text(str(notifyAmntWeek), 'subtitle', Colors.textCol, (3, 45), False)
                elif checkNum(event.unicode):
                    notifyAmntWeek += event.unicode
            if editing3:
                if event.key == pygame.K_BACKSPACE:
                    if len(notifyAmntMonth) > 0:
                        notifyAmntMonth = notifyAmntMonth[:-1]
                elif event.key == pygame.K_RETURN:
                    editing3 = False
                    if len(notifyAmntMonth) == 0:
                        notifyAmntMonth = "None"
                        notifSettings.texts[4] = Text(str(notifyAmntMonth), 'subtitle', Colors.textCol, (3, 60), False)
                elif checkNum(event.unicode):
                    notifyAmntMonth += event.unicode
                    
            if editing4:
                if event.key == pygame.K_BACKSPACE:
                    if len(refreshRate) > 0:
                        refreshRate = refreshRate[:-1]
                elif event.key == pygame.K_RETURN:
                    editing4 = False
                    if len(refreshRate) == 0:
                        refreshRate = "None"
                        notifSettings.texts[7] = Text(str(refreshRate), 'subtitle', Colors.textCol, (3, 60), False)
                elif checkNum(event.unicode):
                    refreshRate += event.unicode
            if editing5:
                if event.key == pygame.K_BACKSPACE:
                    if len(notifRate) > 0:
                        notifRate = notifRate[:-1]
                elif event.key == pygame.K_RETURN:
                    editing5 = False
                    if len(notifRate) == 0:
                        notifRate = "None"
                        notifSettings.texts[8] = Text(str(notifRate), 'subtitle', Colors.textCol, (3, 60), False)
                elif checkNum(event.unicode):
                    notifRate += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in notifSettings.buttons:
                if button.checkMouseOver(pos):
                    if button.onClickFunc != None:
                        button.onClickFunc()

def checkNum(char):
    if str(char) in nums:
        return True

def refresh():
    global dayInfo, weekInfo, monthInfo
    dayInfo = eval(getDayInfo())
    weekInfo = eval(getWeekInfo())
    monthInfo = eval(getMonthInfo())

def refreshAllText():
    fullList.texts = fullList.texts[:1]
    writeFullListDay()
    menu.texts = menu.texts[:4]
    addBiggestDroppersToMenu()

# **
def checkAndQueue():
    refresh()
    # ***find a way to optimize it so its running the least amount of code
    if notifyAmntDay != 'None' and notifyAmntDay != '':
        for dataDict in dayInfo:
            if muteList[dataDict['label']] == False:
                if float(dataDict['perf']) <= -1 * float(notifyAmntDay):
                    if checkNotInQueue([dataDict, 'day']):
                        notifQueue.append([dataDict, 'day'])
    
    if notifyAmntWeek != 'None' and notifyAmntWeek != '':
        for dataDict in weekInfo:
            if muteList[dataDict['label']] == False:
                if float(dataDict['perf']) <= -1 * float(notifyAmntWeek):
                    if checkNotInQueue([dataDict, 'week']):
                        notifQueue.append([dataDict, 'week'])
    
    if notifyAmntMonth != 'None' and notifyAmntMonth != '':
        for dataDict in monthInfo:
            if muteList[dataDict['label']] == False:
                if float(dataDict['perf']) <= -1 * float(notifyAmntMonth):
                    if checkNotInQueue([dataDict, 'month']):
                        notifQueue.append([dataDict, 'month'])

def handleQueue(events):
    for event in events:
        if event.type == pygame.USEREVENT + 1:
            if len(notifQueue) > 0:
                notify("New Target Low!", str(notifQueue[0][0]['label']) + " dropped by " + str(notifQueue[0][0]['perf']) + "% in a " + str(notifQueue[0][1]))
                notifQueue.remove(notifQueue[0])

# **
def checkNotInQueue(newNotif):
    # this function can be optimized to add a bunch of other checks,
    # like if it was notified about today yet or not
    for notif in notifQueue:
        if newNotif[0]['label'] == notif[0]['label'] and newNotif[1] == notif[1]:
            return False
    return True

def getMuteSettings():
    muteList = {}
    for dict in monthInfo:
        muteList[dict['label']] = False
    return muteList

def muteStock():
    muteList[stockBeingViewed] = True
    setupFutureView(stockBeingViewed)

def unMuteStock():
    muteList[stockBeingViewed] = False
    setupFutureView(stockBeingViewed)


# Run Stuff~~~~~~
WIDTH = 600
HEIGHT = 700
pygame.init()
# idling = False
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.RESIZABLE)
Surf.surface = screen
Screen.state = 0
editing1 = False
editing2 = False
editing3 = False
editing4 = False
editing5 = False
nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
notifQueue = []
stockBeingViewed = None
path = getSettingsPath()
data = getJsonData(path)
notifyAmntDay, notifyAmntWeek, notifyAmntMonth = getNotifData(data)
notifyAmntDay = str(notifyAmntDay)
notifyAmntWeek = str(notifyAmntWeek)
notifyAmntMonth = str(notifyAmntMonth)
refreshRate, notifRate = getTimerData(data)
refreshRate = str(refreshRate)
notifRate = str(notifRate)
dayInfo = eval(getDayInfo())
weekInfo = eval(getWeekInfo())
monthInfo = eval(getMonthInfo())
muteList = getMuteSettings()
pygame.time.set_timer(pygame.USEREVENT + 1, int(notifRate)*1000)


# Screens~~~~~~~~~~
menu = Screen(
    [
        Button("View full list", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(34, 21, 32, 10), 20, changeStateToFullList),
        Button("Notification Settings", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(34, 33, 32, 10), 20, changeStateToNotif),
        Button("Idle", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(34, 45, 32, 10), 20, setIdle),
    ],
    [
        Text('Crystal Ball', 'title', Colors.textCol, (50,5), True, True),
        Text('Biggest Droppers', 'subtitle', Colors.textCol, (50,60), True),
        Text('on the day', 'subtitle', Colors.textCol, (30,67), True, True),
        Text('on the week', 'subtitle', Colors.textCol, (70,67), True, True)
    ],
    Colors.bgCol1, Colors.bgCol2
)

fullList = Screen(
    [
        Button("Back", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(40, 88, 20, 9), 20, changeStateToMenu),
        Button("Sort Day", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(16, 13, 18, 5), 20, setFullListDay),
        Button("Sort Week", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(41, 13, 18, 5), 20, setFullListWeek),
        Button("Sort Month", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(66, 13, 18, 5), 20, setFullListMonth)
    ],
    [
        Text("All Futures", 'title', Colors.textCol, (50,2), True, True)
    ],
    Colors.bgCol1, Colors.bgCol2
)

futureView = Screen(
    [
        Button("Back", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(35, 80, 30, 10), 20, changeStateToFullList),
        None

    ],
    [
        None,
        None,
        None,
        None
    ],
    Colors.bgCol1, Colors.bgCol2
)

notifSettings = Screen(
    [
        Button("Back", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(38, 85, 24, 10), 20, writeSettingsAndMenuState),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(5, 36, 16, 7), 20, setEditing1),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(5, 51, 16, 7), 20, setEditing2),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(5, 66, 16, 7), 20, setEditing3),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(52, 43, 16, 7), 20, setEditing4),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(52, 68, 16, 7), 20, setEditing5)
    ],
    [
        Text("Notification Settings", 'title', Colors.textCol, (50, 3), True, True),
        Text("Notify for drops more than", 'subtitle', Colors.textCol, (3, 20), False),
        Text(str(notifyAmntDay) + "% in a day", 'paragraph', Colors.textCol, (3, 30), False),
        Text(str(notifyAmntWeek) + "% in a week", 'paragraph', Colors.textCol, (3, 45), False),
        Text(str(notifyAmntMonth) + "% in a month", 'paragraph', Colors.textCol, (3, 60), False),
        Text("Refresh Rate", 'subtitle', Colors.textCol, (60, 30), True),
        Text("Notification Rate", 'subtitle', Colors.textCol, (60, 55), True),
        Text("Every " + str(refreshRate) + " minutes", 'paragraph', Colors.textCol, (60, 38), True),
        Text("Every " + str(notifRate) + " minutes", 'paragraph', Colors.textCol, (60, 63), True)
    ],
    Colors.bgCol1, Colors.bgCol2
)

idle = Screen(
    [], [], [0,0,0], [0,0,0]
)

# More run stuff~~~~~~~~~~~~
addBiggestDroppersToMenu()
setFullListDay()

fullList.updateFunction = fullListUpdate
fullList.inputFunction = fullListInput
notifSettings.renderFunction = notifSettingsRender
notifSettings.updateFunction = notifSettingsUpdate
notifSettings.inputFunction = notifSettingsInput