import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import addRemoveGetPlayers
import someCoolLights
import APICall
import translateRank

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

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize LCD panel
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Initial state of button
pressed = False
points = 0

# Button toggler
def toggleGameMode(self):
    global pressed
    pressed = True

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
    response = APICall.getResponse(screenName,console,gameMode)

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

    # Get player rank (i.e. Tier 2 Div 3 --> 'B2S3')
    playerRank = translateRank.getRank(tier,division)

    # Format the top row spacing to look nice
    numTopSpaces = 16 - len(str(points)) - len(playerRank) - len(name) - 1
    topSpaces = ''
    for j in range(0,numTopSpaces):
        topSpaces = topSpaces + ' '

    # Compile message
    message = name.title() + topSpaces + playerRank + ' ' + str(points)
    print(message)
    return message

##    gamesUp = 2
##    gamesDown = 4
##    pointsUp = 14
##    pointsDown = 32
##    numBottomSpaces = 16 - len(str(gamesUp)) - len(str(gamesDown)) - 2 - len(str(pointsUp)) - len(str(pointsDown))
##    bottomSpaces = ''
##    for k in range(0,numBottomSpaces):
##        bottomSpaces = bottomSpaces + ' '
##    message = name.title() + topSpaces + playerRank + ' ' + str(points) + '\n' + str(gamesDown) + '|' + str(gamesUp) + bottomSpaces + str(pointsDown) + '|' + str(pointsUp)
##    return message
    

if __name__ == "__main__":
    GPIO.add_event_detect(19,GPIO.FALLING,callback=toggleGameMode,bouncetime=300)
    initialize()







