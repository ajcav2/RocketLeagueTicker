import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import addRemoveGetPlayers
import someCoolLights
import APICall
import translateRank
import RLTrackingParser
import math

# Pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize LCD panel
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Initial state of buttons
pressed = False
needMoreInfo = False

# Initialize points variable
points = 0

# Button toggler
def toggleGameMode(self):
    global pressed
    pressed = True

# Toggle display of extra player stats
def toggleMoreInfo(self):
    global needMoreInfo
    needMoreInfo = True

def initialize():
    # Welcome
    lcd.clear()
    lcd.message('Welcome to RL\nfor RaspberryPi')
    someCoolLights.intro()

    # Create a list of names
    updateNames()

    # Start program in singles
    singles()

def singles():
    global pressed
    GPIO.output(21,True)
    GPIO.output(20,False)
    GPIO.output(16,False)
    GPIO.output(26,False)
    lcd.clear()
    lcd.message('Singles')
    time.sleep(2)
    lcd.clear()
    while not pressed:
        stream(1)
    pressed = False
    doubles()

def doubles():
    global pressed
    GPIO.output(21,True)
    GPIO.output(20,True)
    GPIO.output(16,False)
    GPIO.output(26,False)
    lcd.clear()
    lcd.message('Doubles')
    time.sleep(2)
    lcd.clear()
    while not pressed:
        stream(2)
    pressed = False
    standard()

def standard():
    global pressed
    GPIO.output(21,True)
    GPIO.output(20,True)
    GPIO.output(16,True)
    GPIO.output(26,False)
    lcd.clear()
    lcd.message('Standard')
    time.sleep(2)
    lcd.clear()
    while not pressed:
        stream(3)
    pressed = False
    soloStandard()

def soloStandard():
    global pressed
    GPIO.output(21,True)
    GPIO.output(20,True)
    GPIO.output(16,True)
    GPIO.output(26,True)
    lcd.clear()
    lcd.message('Solo Standard')
    time.sleep(2)
    lcd.clear()
    while not pressed:
        stream(4)
    pressed = False
    singles()

def stream(gameMode):
    global needMoreInfo
    # Get updated name list
    updateNames()

    # Stream information for each player
    for i in range(0,len(names)):
        if not pressed:
            try:
                message = getMessage(names[i],screenNames[i],consoles[i],gameMode)
                lcd.clear()
                lcd.message(message)
                time.sleep(3)
                
            except IndexError:
                return
        if needMoreInfo:
            # User has pressed the GPIO13 button, requesting more information
            # about the current player
            try:
                stats = getPlayerStats(screenNames[i],consoles[i],gameMode)
                lcd.clear()
                
                message = names[i].title() + "\nWins: " + stats[0]
                lcd.message(message)
                time.sleep(3)
                lcd.clear()

                message = names[i].title() + "\nGoals: " + stats[1]
                lcd.message(message)
                time.sleep(3)
                lcd.clear()

                message = names[i].title() + "\nMVPs: " + stats[2]
                lcd.message(message)
                time.sleep(3)
                lcd.clear()

                message = names[i].title() + "\nSaves: " + stats[3]
                lcd.message(message)
                time.sleep(3)
                lcd.clear()

                message = names[i].title() + "\nShots: " + stats[4]
                lcd.message(message)
                time.sleep(3)
                lcd.clear()

                message = names[i].title() + "\nAssists: " + stats[5]
                lcd.message(message)
                time.sleep(3)
                lcd.clear()

                # Reset toggler
                needMoreInfo = False

            except IndexError:
                return

def updateNames():
    # Update player list
    global names
    global screenNames
    global consoles
    namesDict = addRemoveGetPlayers.getPlayers()
    names = []
    screenNames = []
    consoles = []
    for key in namesDict['Items']:
        names.append(key['name'])
        screenNames.append(key['screenName'])
        consoles.append(key['console'])

def getMessage(name,screenName,console,gameMode):
    global points
    GPIO.output(6,True)
    response = APICall.getResponse(screenName,console,gameMode)
    GPIO.output(6,False)

    # Check for errors
    if 'code' in [keys for keys in response]:
        if response['code'] == 404:
            return "Player " + screenName + "\nnot found"
        elif response['code'] == 401:
            return "Invalid API key"
        elif response['code'] == 400:
            return "Invalid request"
        elif response['code'] >= 500:
            return "RL API not\n accessible now"

    # Get playlist
    if (gameMode == 1):
        playlist = '10'
        game = "singles"
    elif (gameMode == 2):
        playlist = '11'
        game = "doubles"
    elif (gameMode == 3):
        playlist = '13'
        game = "standard"
    elif (gameMode == 4):
        playlist = '12'
        game = "solo standard"

    # Get current season
    currentSeason = [season for season in response['rankedSeasons']][0]
    season = response['rankedSeasons'][currentSeason]
    numPlaylists = len([plist for plist in season])
    if numPlaylists < 1:
        return "No ranked stats\n for " + name.title()
    else:
        try:
            if season[playlist] != None:
                # Get information about desired playlist
                points = str(season[playlist]['rankPoints'])
                division = season[playlist]['division']
                tier = season[playlist]['tier']
        except KeyError:
            # User does not have any stats in this playlist
            return "No " + game + "\ninfo for " + name.title()

    # Get player rank (e.g. Tier 2 Div 0 --> 'B2S1')
    playerRank = translateRank.getRank(tier,division)

    # Format the top row spacing to look nice
    numTopSpaces = 16 - len(str(points)) - len(playerRank) - len(name) - 1
    topSpaces = ''
    for j in range(0,numTopSpaces):
        topSpaces = topSpaces + ' '

    # Get data from Rocket League Tracking Network
    GPIO.output(5,True)
    HTMLData = RLTrackingParser.getHTMLData(screenName,console,gameMode)
    GPIO.output(5,False)
    pointsDown = HTMLData[0]
    pointsUp = HTMLData[1]

    # Calculate gamesUp/gamesDown from pointsUp and pointsDown and
    # the average number of points awarder per game
    if (int(pointsDown) != 0 and int(pointsUp != 0)):
        gamesDown = int(math.ceil(int(round(int(pointsDown)))/9) + 1)
        gamesUp = int(math.ceil(int(round(int(pointsUp)))/9) + 1)
    else:
        gamesDown = '-'
        gamesUp = '-'

    # Format the bottom row spacing to look nice
    numBottomSpaces = 16 - len(str(gamesUp)) - len(str(gamesDown)) - 2 - len(str(pointsUp)) - len(str(pointsDown))
    bottomSpaces = ''
    for k in range(0,numBottomSpaces):
        bottomSpaces = bottomSpaces + ' '

    # Compile message
    message = name.title() + topSpaces + playerRank + ' ' + str(points)+ '\n' + str(gamesDown) + '|' + str(gamesUp) + bottomSpaces + str(pointsDown) + '|' + str(pointsUp)
    print(message)
    return message

def getPlayerStats(screenName,console,gameMode):
    # Return everything in the 'stats' section of the API response
    response = APICall.getResponse(screenName,console,gameMode)
    stats = []
    stats.append(str(response['stats']['wins']))
    stats.append(str(response['stats']['goals']))
    stats.append(str(response['stats']['mvps']))
    stats.append(str(response['stats']['saves']))
    stats.append(str(response['stats']['shots']))
    stats.append(str(response['stats']['assists']))
    return stats
    

if __name__ == "__main__":
    GPIO.add_event_detect(19,GPIO.FALLING,callback=toggleGameMode,bouncetime=300)
    GPIO.add_event_detect(13,GPIO.FALLING,callback=toggleMoreInfo,bouncetime=300)
    initialize()







