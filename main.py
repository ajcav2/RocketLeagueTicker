import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import addRemoveGetPlayers
import streamer

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

# Create a list of names
namesDict = addRemoveGetPlayers.getPlayers()
names = []
for key in namesDict['Items']:
    names.append(key['name'])

# Initial state of button
pressed = False

# Button toggler
def buttonPress(self):
    global pressed
    pressed = True

def addRemovePlayer(self):
    global names

    # Detemine if user wishes to add or remove a player
    addRemove = ''
    while (addRemove != 'add' and addRemove != 'remove' and addRemove != 'cancel'):
        addRemove = raw_input('Would you like to add or remove a player? (add/remove/cancel): ')

    # Add a player
    if (addRemove == 'add'):
        addRemoveGetPlayers.addPlayer()

    # Remove a player
    elif (addRemove == 'remove'):
        addRemoveGetPlayers.removePlayer()
        
    else: # Cancel the interaction
        print("Cancelled.")
        return
    
    # Wait for DynamoDB to update
    time.sleep(5)
    
    # Regenerate name list
    namesDict = addRemoveGetPlayers.getPlayers()
    names = []
    for key in namesDict['Items']:
        names.append(key['name'])
        

def initialize():
    lcd.clear()
    lcd.message('Welcome to RL\nfor RaspberryPi')
    time.sleep(3)
    singles()

def singles():
    global pressed
    global names
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
    global names
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
    if gameMode == 1:
        for name in names:
            if not pressed:
                try:
                    points = 999 # will be getPoints(player)
                    message = name.title() + ' ' + str(points) + '\n3|8    14|22'
                    lcd.message(message)
                    time.sleep(3)
                    lcd.clear()
                except IndexError:
                    return
    elif gameMode == 2:
        for name in names:
            if not pressed:
                try:
                    points = 999 # will be getPoints(player)
                    playerRank = 'G1D2' # will be getRank(player)
                    gamesUp = 2 # getGamesUp
                    gamesDown = 4 # getGamesDown
                    pointsUp = 14 # getPointsUp
                    pointsDown = 32 # getPointsDown
                    numTopSpaces = 16 - len(str(points)) - len(playerRank) - len(name) - 1
                    topSpaces = ''
                    for j in range(0,numTopSpaces):
                        topSpaces = topSpaces + ' '
                    numBottomSpaces = 16 - len(str(gamesUp)) - len(str(gamesDown)) - 2 - len(str(pointsUp)) - len(str(pointsDown))
                    bottomSpaces = ''
                    for k in range(0,numBottomSpaces):
                        bottomSpaces = bottomSpaces + ' '
                    message = name.title() + topSpaces + playerRank + ' ' + str(points) + '\n' + str(gamesDown) + '|' + str(gamesUp) + bottomSpaces + str(pointsDown) + '|' + str(pointsUp)
                    lcd.message(message)
                    time.sleep(3.5)
                    lcd.clear()
                except IndexError:
                    return
    elif gameMode == 3:
        for i in range(0,len(players.names)):
            if not pressed:
                lcd.message(players.names[i])
                time.sleep(3.5)
                lcd.clear()
##        for i in range(0,len(players.names)):
##            if not pressed:               
##                try:                                 ################
##                  lcd.message(getMessage(player))    # EXAMPLE CODE #
##                  time.sleep(3)                      ################
##                  lcd.clear()
##                except IndexError:
##                    return
    else:
        lcd.message('Solo standard\nstreamer')
        time.sleep(1)
        lcd.clear()

##def getMessage(player):
##    playerName = player
##    screenName = addRemoveGetPlayers...
##    allPlayerInfo = callToAPI(screenName)
##    playerRank = allPlayerInfo[1]
##    gamesUp = allPlayerInfo[2]
##    gamesDown = allPlayerInfo[3]
##    pointsUp = allPlayerInfo[4]
##    pointsDown = allPlayerInfo[5]
##    numTopSpaces = 16 - len(str(points)) - len(playerRank) - len(players.names[i]) - 1
##    topSpaces = ''
##    for j in range(0,numTopSpaces):
##        topSpaces = topSpaces + ' '
##    numBottomSpaces = 16 - len(str(gamesUp)) - len(str(gamesDown)) - 2 - len(str(pointsUp)) - len(str(pointsDown))
##    bottomSpaces = ''
##    for k in range(0,numBottomSpaces):
##        bottomSpaces = bottomSpaces + ' '
##    message = players.names[i] + topSpaces + playerRank + ' ' + str(points) + '\n' + str(gamesDown) + '|' + str(gamesUp) + bottomSpaces + str(pointsDown) + '|' + str(pointsUp)
##    return message

GPIO.add_event_detect(19,GPIO.FALLING,callback=buttonPress,bouncetime=300)
GPIO.add_event_detect(13,GPIO.FALLING,callback=addRemovePlayer,bouncetime=300)
initialize()







