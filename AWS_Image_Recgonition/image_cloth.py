import boto3
# import RPi.GPIO as GPIO
import time

CONTROL_PIN = 17
PWM_FREQ = 50
STEP=60
labellist=['Shirt', 'Shorts', 'Coat', 'Pants', 'Long Sleeve']
# 0: openside, 1: Shirt, 2: Shorts, 3: Coat, 4: Pants, 5: Long Sleeve

def angle_to_duty_cycle(angle=0):
	duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
	return duty_cycle

def rotate(angle):
	
	GPIO.setmode(GPIO.BCM)
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
	rot = tostate - nowstate
	if (rot > 180):
		rot = - (360 - rot)
	elif (rot < -180):
		rot = 360 + rot
	return 60 * rot


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
			# result.append(labellist.index(label['Name']))
			result = labellist.index(label['Name'])
			print (label['Name'] + ' : ' + str(label['Confidence']))
			break
	return result

if __name__ == "__main__":

	imageFile=['img/redtshirt.jpg',
				'img/whiteshirt.jpg',
				'img/bluelongshirts.jpg',
				'img/grayjacket.jpg',
				'img/blackpants.jpg',
				'img/shorts.jpg'
				]
	# nowstate = 6 # openside
	resultstate = detect(imageFile[2]) + 1
	# angle = statetoangle(nowstate, resultstate)
	# nowstate = resultstate
	# rotate(0)
	# print("state: " + str(resultstate) + " angle: " + str(angle))
	# rotate(angle)
	print("Result: " + str(resultstate))
	print('Done...')