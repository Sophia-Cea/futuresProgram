import queue
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
# add a setting to customize refresh frequrncy and notification frequency
# add a page that lists all the futures that were notified about
# improve overall ui/change color palette
# improve settings.json so it writes default settings to it if its empty
# make it write changed settings to settings



# Functions for screens~~~~~~~

def changeStateToFullList():
    Screen.state = 1

def changeStateToMenu():
    Screen.state = 0

def changeStateToFutureView():
    Screen.state = 2

def changeStateToNotif():
    Screen.state = 3

def setupFutureView(name):
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
            pygame.draw.rect(screen, Colors.textCol, text.rect, 3, 0)

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
        print("didnt work")
    return path

def getSettingsPath():
    try:
        path = pox.find('settings.json')[0]
    except:
        print("excepting...")
        path = pickNewFilePath()
    return path

def setEditing1():
    global editing1, editing2, editing3, notifyAmntDay
    if editing1:
        editing1 = False
        if len(notifyAmntDay) == 0:
            notifyAmntDay = "None"
            notifSettings.texts[2] = Text(str(notifyAmntDay), 'subtitle', Colors.textCol, (3, 30), False)
    else:
        editing1 = True
        editing2 = False
        editing3 = False
        if notifyAmntDay == "None":
            notifyAmntDay = ""

def setEditing2():
    global editing1, editing2, editing3, notifyAmntWeek
    if editing2:
        editing2 = False
        if len(notifyAmntWeek) == 0:
            notifyAmntWeek = "None"
            notifSettings.texts[3] = Text(str(notifyAmntWeek), 'subtitle', Colors.textCol, (3, 30), False)
    else:
        editing1 = False
        editing2 = True
        editing3 = False
        if notifyAmntWeek == "None":
            notifyAmntWeek = ""

def setEditing3():
    global editing1, editing2, editing3, notifyAmntMonth
    if editing3:
        editing3 = False
        if len(notifyAmntMonth) == 0:
            notifyAmntMonth = "None"
            notifSettings.texts[4] = Text(str(notifyAmntMonth), 'subtitle', Colors.textCol, (3, 30), False)
    else:
        editing1 = False
        editing2 = False
        editing3 = True
        if notifyAmntMonth == "None":
            notifyAmntMonth = ""

def notifSettingsRender(screen):
    screen.blit(pygame.transform.scale(notifSettings.bg, screen.get_size()), (0,0))
    for button in notifSettings.buttons:
        button.draw(screen)
    for text in notifSettings.texts:
        text.draw(screen)
    pygame.draw.line(screen, Colors.textCol, (screen.get_width()/100*10, screen.get_height()/100*12), (screen.get_width()/100*90, screen.get_height()/100*12), 5)
    if editing1:
        pygame.draw.line(screen, (180,50,60), (screen.get_width()/100*3, screen.get_height()/100*35), (screen.get_width()/100*40, screen.get_height()/100*35), 5)
    if editing2:
        pygame.draw.line(screen, (180,50,60), (screen.get_width()/100*3, screen.get_height()/100*50), (screen.get_width()/100*40, screen.get_height()/100*50), 5)
    if editing3:
        pygame.draw.line(screen, (180,50,60), (screen.get_width()/100*3, screen.get_height()/100*65), (screen.get_width()/100*40, screen.get_height()/100*65), 5)

def notifSettingsUpdate():
    pos = pygame.mouse.get_pos()
    for button in notifSettings.buttons:
        if button.checkMouseOver(pos):
            button.hovering = True
        else:
            button.hovering = False
    if editing1:
        notifSettings.texts[2] = Text(str(notifyAmntDay) + "% in a day", 'subtitle', Colors.textCol, (3, 30), False)
    if editing2:
        notifSettings.texts[3] = Text(str(notifyAmntWeek) + "% in a week", 'subtitle', Colors.textCol, (3, 45), False)
    if editing3:
        notifSettings.texts[4] = Text(str(notifyAmntMonth) + "% in a month", 'subtitle', Colors.textCol, (3, 60), False)

def notifSettingsInput(events):
    global notifyAmntDay, notifyAmntMonth, notifyAmntWeek, editing1, editing2, editing3
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

def checkAndQueue():
    refresh()
    # loop thru all the info to find if anything matches notifyAmnts 
    # if it does, add it to the queue
    # make a separate function to deal with notifying from the queue

    #make a function to check day, week, and month data
    for dataDict in dayInfo:
        if float(dataDict['perf']) <= -1 * float(notifyAmntDay):
            # make a function to check its not already in the queue
            notifQueue.append([dataDict, 'day'])
            print(notifQueue)

def handleQueue(events):
    for event in events:
        if event.type == pygame.USEREVENT + 1:
            if len(notifQueue) > 0:
                print("notifying...")
                notify("New Target Low!", str(notifQueue[0][0]['label']) + " dropped by " + str(notifQueue[0][0]['perf']) + "% in a " + str(notifQueue[0][1]))
                notifQueue.remove(notifQueue[0])

# Run Stuff~~~~~~

WIDTH = 600
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.RESIZABLE)
Surf.surface = screen
Screen.state = 0
editing1 = False
editing2 = False
editing3 = False
nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
notifQueue = []
pygame.time.set_timer(pygame.USEREVENT + 1, 5000)

path = getSettingsPath()
print(path)
notifyAmntDay, notifyAmntWeek, notifyAmntMonth = getJsonData(path)
notifyAmntDay = str(notifyAmntDay)
notifyAmntWeek = str(notifyAmntWeek)
notifyAmntMonth = str(notifyAmntMonth)


dayInfo = eval(getDayInfo())
weekInfo = eval(getWeekInfo())
monthInfo = eval(getMonthInfo())



# Screens~~~~~~~~~~

menu = Screen(
    [
        Button("View full list", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(34, 28, 32, 10), 20, changeStateToFullList),
        Button("Notification Settings", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(34, 40, 32, 10), 20, changeStateToNotif)
    ],
    [
        Text('Future Tracking', 'title', Colors.textCol, (50,5), True),
        Text('Biggest Droppers', 'subtitle', Colors.textCol, (50,60), True),
        Text('on the day', 'subtitle', Colors.textCol, (30,67), True),
        Text('on the week', 'subtitle', Colors.textCol, (70,67), True)
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
        Text("All Futures", 'title', Colors.textCol, (50,2), True)
    ],
    Colors.bgCol1, Colors.bgCol2
)

futureView = Screen(
    [
        Button("Back", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(35, 80, 30, 10), 20, changeStateToFullList)

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
        Button("Back", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(38, 85, 24, 10), 20, changeStateToMenu),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(5, 36, 16, 7), 20, setEditing1),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(5, 51, 16, 7), 20, setEditing2),
        Button("Change", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(5, 66, 16, 7), 20, setEditing3)
    ],
    [
        Text("Notification Settings", 'title', Colors.textCol, (50, 3), True),
        Text("Notify for drops more than", 'subtitle', Colors.textCol, (3, 20), False),
        Text(str(notifyAmntDay) + "% in a day", 'subtitle', Colors.textCol, (3, 30), False),
        Text(str(notifyAmntWeek) + "% in a week", 'subtitle', Colors.textCol, (3, 45), False),
        Text(str(notifyAmntMonth) + "% in a month", 'subtitle', Colors.textCol, (3, 60), False)
    ],
    Colors.bgCol1, Colors.bgCol2
)


# More run stuff~~~~~~~~~~~~

addBiggestDroppersToMenu()
setFullListDay()

fullList.updateFunction = fullListUpdate
fullList.inputFunction = fullListInput

notifSettings.renderFunction = notifSettingsRender
notifSettings.updateFunction = notifSettingsUpdate
notifSettings.inputFunction = notifSettingsInput
