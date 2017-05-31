import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
from players import names
from players import screenNames

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 8

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


GPIO.setmode(GPIO.BCM)

GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.output(21,True)
GPIO.output(20,False)
GPIO.output(16,False)
GPIO.output(26,False)
time.sleep(1)
ledCount = 1
stocks = ("LMT","INTC","AMD","CRM","DE","NVDA","TSLA","BA")
lcd.clear()

lcd.message('Welcome to\nRL app')
time.sleep(3)
lcd.clear()
lcd.message('Singles')
time.sleep(3)
lcd.clear()

    #21 20 16 26

while True:
    input_state = GPIO.input(19)
    if input_state == False:
        if ledCount == 1:
            ledCount = ledCount + 1
            GPIO.output(20,True)
            lcd.message('Doubles')
            stocks = ("LMT","INTC")
            time.sleep(2)
            lcd.clear()
        elif ledCount == 2:
            ledCount = ledCount + 1
            GPIO.output(16,True)
            time.sleep(0.25)
            lcd.message('Standard')
            stocks = ("LMT","INTC","AMD")
            time.sleep(2)
            lcd.clear()
        elif ledCount == 3:
            ledCount = ledCount + 1
            GPIO.output(26,True)
            time.sleep(0.25)
            lcd.message('Solo standard')
            stocks = ("BA","TSLA","NVDA")
            time.sleep(2)
            lcd.clear()
        else:
            ledCount = 1
            GPIO.output(20,False)
            GPIO.output(16,False)
            GPIO.output(26,False)
            time.sleep(0.25)
            lcd.message('Singles')
            stocks = ("LMT")
            time.sleep(2)
            lcd.clear()



        
