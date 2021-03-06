#!/usr/bin/python
# import required libraries

import qrcode
from PIL import ImageDraw
from PIL import Image
from signal import signal, SIGTERM,SIGHUP , pause
from rpi_lcd import LCD
import ST7735 as TFT
import http.client as connec
import RPi.GPIO as GPIO2
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import json
import time

state=0
count=5
#start PWM running, but with value of 0 (pulse off)


# these GPIO pins are connected to the keypad
# change these according to your connections!
L1 = 5
L2 = 6
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000


# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# BeagleBone Black configuration.
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))


# Initialize the GPIO pins
GPIO2.setwarnings(False)
GPIO2.setmode(GPIO2.BCM)
GPIO2.setup(4,GPIO2.OUT)
GPIO2.setup(L1, GPIO2.OUT)
GPIO2.setup(L2, GPIO2.OUT)
GPIO2.setup(L3, GPIO2.OUT)
GPIO2.setup(L4, GPIO2.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors
servo1 = GPIO2.PWM(4,50)
servo1.start(0)
GPIO2.setup(C1, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)
GPIO2.setup(C2, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)
GPIO2.setup(C3, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)
def servorot():
      #start PWM running, but with value of 0 (pulse off)
    print ("Waiting for 2 seconds")
    time.sleep(2)

#Let's move the servo!
    print ("Rotating 180 degrees in 10 steps")

# Define variable duty
    duty = 2

# Loop for duty values from 2 to 12 (0 to 180 degrees)
    while duty <= 12:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.01)
        duty = duty + 1

# Wait a couple of seconds
    time.sleep(2)

# Turn back to 90 degrees
    print ("Turning back to 90 degrees for 2 seconds")
    servo1.ChangeDutyCycle(7)
    time.sleep(0.1)

#turn back to 0 degrees
    print ("Turning back to 0 degrees")
    servo1.ChangeDutyCycle(2)
    time.sleep(2)
    servo1.ChangeDutyCycle(0)
def turnup():
#Let's move the servo!
    print ("Rotating 180 degrees in 10 steps")

# Define variable duty
    duty = 2

# Loop for duty values from 2 to 12 (0 to 180 degrees)
    while duty <= 12.5:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.05)
        duty = duty + 1

# Wait a couple of seconds
    time.sleep(2)
    servo1.ChangeDutyCycle(0)
def turndown():
# Turn back to 90 degrees
    print ("Turning back to 90 degrees for 2 seconds")
    servo1.ChangeDutyCycle(7)
    time.sleep(0.1)

#turn back to 0 degrees
    print ("Turning back to 0 degrees")
    servo1.ChangeDutyCycle(2)
    time.sleep(2)
    servo1.ChangeDutyCycle(0)
    
def dispenser(c):
    
    global state
    for counter in range(c):
        if(c==120):
            turndown()
            time.sleep(1)
            break
        if( state==1):
            turndown()
            state=0
        else:
            turnup()
            state=1
    

#Clean things up at the end

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column
#initiate lcd
lcd=LCD()
servorot()
lcd.text("smart-vend",1)
time.sleep(1)
lcd.clear()
def post(data):
  conn = connec.HTTPSConnection('smart-vend.herokuapp.com')
  conn.request("POST", "/", data , {'Content-Type': 'application/json'})
  resp= conn.getresponse().status
  return resp

charac=[]
data2=[]
data=None
def readLine(line, characters):
    GPIO2.output(line, GPIO2.HIGH)
    if(GPIO2.input(C1) == 1):
        if(line!=L4): 
         charac.append(characters[0])
         lcd.text("".join(charac),2)
        else:
         charac.clear()
         data2.clear()
         lcd.clear()
         lcd.text("Enter the product no",1)
    if(GPIO2.input(C2) == 1):
        charac.append(characters[1])
        lcd.text("".join(charac),2)
    if(GPIO2.input(C3) == 1):
        if(line!=L4):
                charac.append(characters[2])
                lcd.text("".join(charac),2)
        elif(len(charac)==0 ):
                lcd.text('Enter a valid value ',2)
        else:
                data="".join(charac)
                print(data)
                lcd.clear()
                charac.clear()
                data2.append(data)
                print(data2)
    GPIO2.output(line, GPIO2.LOW)

try:
    disp.begin()
    
    
    while True:
       print('Enter the product number')
       lcd.text('Enter product no.',1)
       while (len(data2)==0):
        # call the readLine function for each row of the keypad
           readLine(L1, ["1","2","3"])
           readLine(L2, ["4","5","6"])
           readLine(L3, ["7","8","9"])
           readLine(L4, ["*","0","#"])
           time.sleep(0.2)
       if (data2[0]!='1'):
           data2.clear()
           print(data2)
           lcd.text("No product",1)
           time.sleep(2)
       else:
           print("Enter the quantity")
           lcd.text('Enter the quantity',1)
       while (len(data2)==1):
           if not int(data2[0]) :
                           lcd.text('Enter a valid product',1)
                           data2.clear()
           else:
                           readLine(L1, ["1","2","3"])
                           readLine(L2, ["4","5","6"])
                           readLine(L3, ["7","8","9"])
                           readLine(L4, ["*","0","#"])
                           time.sleep(0.2)
       if(len(data2)==2):
           if not int(data2[1]):
                           lcd.text('Enter a valid quantity',1)
                           data2.clear()
           else:  
                           sum = int(data2[0])* int(data2[1])
                           data2.append(sum)
                           jsonfile={'item':data2[0],'quantity':data2[1],'amount':sum*100}
                           print(jsonfile)
                           flag=True
                           count=0
                           starttime = time.time()
                           while (flag and count<9):
                                      displ= "Pay"+" "+str(sum)+"RS"
                                      lcd.text(displ,1)
                                      time.sleep(2)
                                      lcd.text('Waiting payment',2)
                                      image = qrcode.make('upi://pay?ver=01&mode=01&pa=rpy.qrsmarted07480129793@icici&pn=smarted&tr=RZPJgv9V3PgSn6e1sqrv2&tn=Paymenttosmarted&am='+str(sum)+'&cu=INR&mc=5045&qrMedium=04')
                                      image = image.rotate(90).resize((WIDTH, HEIGHT))
                                      print('Drawing image')
                                      disp.display(image)
                                      time.sleep(15.0 - ((time.time() - starttime) % 15))
                                      response=post(json.dumps(jsonfile))
                                      if(response==200):
                                                        flag=False
                                                        lcd.clear()
                                                        lcd.text('Payment Successful',1)
                                                        time.sleep(5)
                                                        disp.clear()
                                                        lcd.clear()
                                                        lcd.text('Vending...',1)
                                                        dispenser(int(data2[1]))
                                                        time.sleep(2)
                                                        lcd.text('Thank You',1)
                                                        time.sleep(2)
                                                        lcd.clear()
                                                        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
                                                        disp.display(img)

                                      count=count+1
                           if(response==504): 
                                      lcd.text('payment failed',1)
                                      time.sleep(2)
                                      lcd.clear()
                           print(response)
                           time.sleep(1)
                           data2.clear() 
except KeyboardInterrupt:
    print("\nApplication stopped!")
    lcd.clear()
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    disp.display(img)
    servo1.stop()
    GPIO2.cleanup()
    print("Servo Stop")
