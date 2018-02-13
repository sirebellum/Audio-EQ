import socket
import RPi.GPIO as GPIO


UDP_IP = "172.24.143.104"
UDP_PORT = 9900

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Sets naming convention for pins
GPIO.setmode(GPIO.BCM)

# Prevent warnings from printing, who needs 'em!
GPIO.setwarnings(False)

# Set GPIO pins as outputs
GPIO.setup(18,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)

engage=1
GPIO.output(18,GPIO.HIGH)
GPIO.output(10,GPIO.LOW)

while True:
	#listen to port for package
	data = sock.recv(1024)
	print (data)
	if data == "ENGAGE":
		# rec LED on
		GPIO.output(18,GPIO.LOW)
		# standby LED off
		GPIO.output(10,GPIO.HIGH)
		engage = 0
		# Delay for testing purposes
		# time.sleep(1)

	elif data == "DISENGAGE":
		# rec LED off
		GPIO.output(18,GPIO.HIGH)
		# standby LED on
		GPIO.output(10,GPIO.LOW)
		engage = 1
		# Delay for testing porpoises
		# time.sleep(1)

	else:
		GPIO.output(18,GPIO.HIGH)
		GPIO.output(10,GPIO.HIGH)
