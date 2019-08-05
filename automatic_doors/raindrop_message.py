import time
import RPi.GPIO as GPIO
import socket
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
count=0
host=192.168.209.178
port=12345
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True
	state=GPIO.input(4)
	
	if(state==0)
		print(Water Detected!)
		count=count+1
		print(count)
		if(count==2)
			print(alarm)
			s.sendall(b'Water Detected!')
			data = s.recv(1024)
			print('Received', repr(data))
	else
		print(Dry)
		count=0
	time.sleep(5)