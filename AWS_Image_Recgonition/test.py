import RPi.GPIO as GPIO
import picamera
import time
import boto3
import serial
import sys
from time import sleep

# for arduino
port = "/dev/ttyUSB0"
s1 = serial.Serial(port,9600)

# for pi_camera
GPIO.setmode(GPIO.BOARD)
buttonPin = 3
GPIO.setup(buttonPin, GPIO.IN)
prev_input = 1

# for motor
CONTROL_PIN = 11
PWM_FREQ = 50
STEP=60

class Scanner:
    def __init__(self, URL=0):
        self.Frame = []
        self.status = False
        self.isstop = False

        self.capture = picamera.PiCamera()
        time.sleep(2)
        self.start()

    def start(self):
        print("ipcom started!!")

    def stop(self):
        self.isstop = True
        print("ipcom stopped!!")

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def get_photo(self, filename):
        self.capture.capture(filename)


def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def rotate(angle):
    # GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN, GPIO.OUT)
    
    pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
    pwm.start(0)

    dc = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(dc)
    print('角度={: >3}, 工作週期={:.2f}'.format(angle, dc))
    time.sleep(2)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    time.sleep(2)
    pwm.stop()

def statetoangle(nowstate, tostate):
    # rot = tostate - nowstate
    # if (rot > 180):
    #     rot = - (360 - rot)
    # elif (rot < -180):
    #     rot = 360 + rot
    if(tostate < 4):
        rotate(0)
        time.sleep(10)
        rot = tostate * 60 - 10
    else:
        rotate(180)
        if( tostate == 4):
            rot = 50
        else:
            rot = 110
    return rot


def detect(imageFile):
    # result=[]
    client=boto3.client('rekognition')
   
    with open(imageFile, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    print(imageFile + ': ')
    print('Detected labels in ' + imageFile)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        if(label['Name'] in labellist):
            result = labellist.index(label['Name'])
            print (label['Name'] + ' : ' + str(label['Confidence']))
            break
        else:
            result = -1
    return result

def callduinorotate(mode):
    if mode == 1:
        print('Degree is 50L.')
        s1.write(b'deg0\n')
        sleep(3)
        s1.write(b'deg50\n')
        sleep(3)
        s1.write(b'deg45\n')
        sleep(0.5)
    elif mode == 2:
        print('Degree is 110L.')
        s1.write(b'deg0\n')
        sleep(3)
        s1.write(b'deg110\n')
        sleep(3)
        s1.write(b'deg45\n')
        sleep(0.5)
    elif mode == 3:
        print('Degree is 170L.')
        s1.write(b'deg0\n')
        sleep(3)
        s1.write(b'deg170\n')
        sleep(3)
        s1.write(b'deg45\n')
        sleep(0.5)
    elif mode == 4:
        print('Degree is 50R.')
        s1.write(b'deg180\n')
        sleep(3)
        s1.write(b'deg50\n')
        sleep(3)
        s1.write(b'deg135\n')
        sleep(0.5)
    elif mode == 5:
        print('Degree is 110R.')
        s1.write(b'deg180\n')
        sleep(3)
        s1.write(b'deg110\n')
        sleep(3)
        s1.write(b'deg135\n')
        sleep(0.5)
    else:
        print('command error!')

    while s1.in_waiting:
        feedback = s1.readline().decode()
        print('reply: ',feedback)


s = Scanner()
n = 0
imageFile=['img/redtshirt.jpg',
            'img/whiteshirt.jpg',
            'img/bluelongshirts.jpg',
            'img/grayjacket.jpg',
            'img/blackpants.jpg',
            'img/shorts.jpg'
            ]
labellist=['Shirt', 'Shorts', 'Coat', 'Pants', 'Long Sleeve']
# 0: openside, 1: Shirt, 2: Shorts, 3: Coat, 4: Pants, 5: Long Sleeve
nowstate = 0 # openside

while True:
    input = GPIO.input(buttonPin)
    if((not prev_input) and input):
        print("Button pressed")
        s.get_photo("photo/photo%d.png"%n)
        print(n)
        resultstate = detect("photo/photo%d.png"%n) + 1
        if(resultstate != 0):
            # use rpi to rotate
            # angle = statetoangle(nowstate, resultstate)
            # nowstate = resultstate
            # rotate(0)
            # print("state: " + str(resultstate) + " angle: " + str(angle))
            # rotate(angle)
            # print(result)

            # use arduino to rotate
            # callduinorotate(resultstate)
            print('Done...')
            n = n + 1
        else:
            print('Cannot detect, please try again')

    prev_input = input
    time.sleep(0.05)
