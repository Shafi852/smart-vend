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


GPIO2.setup(L1, GPIO2.OUT)
GPIO2.setup(L2, GPIO2.OUT)
GPIO2.setup(L3, GPIO2.OUT)
GPIO2.setup(L4, GPIO2.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO2.setup(C1, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)
GPIO2.setup(C2, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)
GPIO2.setup(C3, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column
#initiate lcd
lcd=LCD()
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
        charac.append(characters[0])
        lcd.text("".join(charac),2)
    if(GPIO2.input(C2) == 1):
        charac.append(characters[1])
        lcd.text("".join(charac),2)
    if(GPIO2.input(C3) == 1):
        if(line!=L4):
                charac.append(characters[2])
                lcd.text("".join(charac),2)
        elif(len(charac)==0):
                lcd.text('Enter a valid value',2)
        else:
                data="".join(charac)
                print(data)
                lcd.clear()
                charac.clear()
                data2.append(data)
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
       print("Enter the quantity")
       lcd.text('Enter the quantity',1)
       while (len(data2)==1):
           if not int(data2[0]):
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
                           while (flag and count<2):
                                      displ= "Pay"+" "+str(sum)+"RS"
                                      lcd.text(displ,1)
                                      lcd.text('Waiting payment',1)
                                      image = qrcode.make('upi://pay?ver=01&mode=01&pa=rpy.qrvednor996918870966@icici&pn=Vednor&tr=RZPJZmCi4hEGJIf0Aqrv2&am='+str(sum)+'&tn=PaymenttoVednor&cu=INR&mc=7372&qrMedium=04')
                                      image = image.rotate(90).resize((WIDTH, HEIGHT))
                                      print('Drawing image')
                                      disp.display(image)
                                      time.sleep(15.0 - ((time.time() - starttime) % 15))
                                      response=post(json.dumps(jsonfile))
                                      if(response==200):
                                                        flag=False
                                                        lcd.text('Payment Successful',1)
                                                        time.sleep(3)
                                                        disp.clear()
                                                        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
                                                        disp.display(img)

                                      count=count+1
                           if(response==503): 
                                      lcd.text('payment failed',1)
                           print(response)
                           time.sleep(1)
                           data2.clear() 
except KeyboardInterrupt:
    print("\nApplication stopped!")
    lcd.clear()
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    disp.display(img)
