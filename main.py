import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import players

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

def buttonPress(self):
    global pressed
    pressed = True

def initialize():
    lcd.clear()
    lcd.message('Welcome to\nRL app')
    time.sleep(3)
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
    if gameMode == 1:
        lcd.message('Singles\nstreamer')
        time.sleep(1)
        lcd.clear()
    elif gameMode == 2:
        lcd.message('Doubles\nstreamer')
        time.sleep(1)
        lcd.clear()
    elif gameMode == 3:
        lcd.message('Standard\nstreamer')
        time.sleep(1)
        lcd.clear()
    else:
        lcd.message('Solo standard\nstreamer')
        time.sleep(1)
        lcd.clear()

GPIO.add_event_detect(19,GPIO.FALLING,callback=buttonPress,bouncetime=300)
initialize()
    





    
