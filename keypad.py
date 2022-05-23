# import required libraries
import http.client as connec
import RPi.GPIO as GPIO
import json
import time

# these GPIO pins are connected to the keypad
# change these according to your connections!
L1 = 25
L2 = 8
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20


# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column
def post(data):
  conn = connec.HTTPSConnection('eoev19ctpl8p7i5.m.pipedream.net')
  conn.request("POST", "/", data , {'Content-Type': 'application/json'})
  resp= conn.getresponse().status
  print(resp)


charac=[]
data2=[]
data=None
def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        charac.append(characters[0])
    if(GPIO.input(C2) == 1):
        charac.append(characters[1])
    if(GPIO.input(C3) == 1):
        if(line!=L4):
                charac.append(characters[2])
        else:
                data="".join(charac)
                print(data)
                charac.clear()
                data2.append(data)
    GPIO.output(line, GPIO.LOW)

try:
    while True:
       print('Enter the product number')
       while (len(data2)==0):
        # call the readLine function for each row of the keypad
           readLine(L1, ["1","2","3"])
           readLine(L2, ["4","5","6"])
           readLine(L3, ["7","8","9"])
           readLine(L4, ["*","0","#"])
           time.sleep(0.2)
       print("Enter the quantity")
       while (len(data2)==1):
           if not int(data2[0]):
                           print('Enter a valid product')
                           data2.clear()
           else:
                           readLine(L1, ["10","5","3"])
                           readLine(L2, ["4","5","6"])
                           readLine(L3, ["7","8","9"])
                           readLine(L4, ["*","0","#"])
                           time.sleep(0.2)
       if(len(data2)==2):
           if not int(data2[1]):
                           print('Enter a valid quantity')
           else:  
                           sum = int(data2[0])* int(data2[1])
                           data2.append(sum)
                           jsonfile={'item':data2[0],'quantity':data2[1],'amount':sum}
                           print(jsonfile)
                           data2.clear() 
except KeyboardInterrupt:
    print("\nApplication stopped!")
