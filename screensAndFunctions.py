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



# Run Stuff~~~~~~

WIDTH = 600
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.RESIZABLE)
Surf.surface = screen
Screen.state = 0

path = getSettingsPath()
print(path)
notifyAmnt = getJsonData(path)


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
        Button("Back", Colors.textCol, Colors.buttonCol1, Colors.buttonCol2, pygame.Rect(38, 85, 24, 10), 20, changeStateToMenu)
    ],
    [
        Text("Notification Settings", 'title', Colors.textCol, (50, 3), True),
        Text("Notify for drops more than: " + str(notifyAmnt), 'paragraph', Colors.textCol, (5, 25), False)
    ],
    Colors.bgCol1, Colors.bgCol2
)



addBiggestDroppersToMenu()
setFullListDay()

fullList.updateFunction = fullListUpdate
fullList.inputFunction = fullListInput
