from flask import Flask,render_template,request
import sys
import time
import RPi.GPIO as GPIO
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
StepPins = [18,22,23,24]
for pin in StepPins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, False)
if len(sys.argv)>1:
	WaitTime = int(sys.argv[1])/float(8000)
else:
	WaitTime = 10/float(8000)
 
Seq = [[1,0,0,1],
	[1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1]]
Sep = [[0,0,0,1],
	[0,0,1,1],
	[0,0,1,0],
	[0,1,1,0],
	[0,1,0,0],
	[1,1,0,0],
	[1,0,0,0],
	[1,0,0,1]]
 
mode=0
def doorset(md) :
	StepCounter = 0
        StepCount = len(Seq)
        StepCount2 = len(Sep)
        StepDir = 1
        timecount=0
	while(True) :
            if md == 0 :
                for pin in range(0,4):
                        xpin = StepPins[pin]
                        if Seq[StepCounter][pin] != 0:
                                GPIO.output(xpin, True)
                        else:
                                GPIO.output(xpin, False)
 
                StepCounter += StepDir
 
                if StepCounter>=StepCount:
                        StepCounter = 0
                if StepCounter<0 :
                        StepCounter = StepCount+StepDir
 
 
                time.sleep(WaitTime)
                timecount=timecount+1;
                if timecount == 9000 :
                    md=1;
                    return;
            if md == 1 :
                for pin in range(0,4):
                        xpin = StepPins[pin]
                        if Sep[StepCounter][pin] != 0:
                                GPIO.output(xpin, True)
                        else:
                                GPIO.output(xpin, False)
 
                StepCounter += StepDir
 
                if StepCounter>=StepCount2:
                        StepCounter = 0
                if StepCounter<0 :
                        StepCounter = StepCount2+StepDir
 
                
                time.sleep(WaitTime)
                timecount=timecount+1;
                if timecount == 12000 :
                    md=1;
                    return;
 
 
 
 
@app.route("/")
def main():
    gpiostate={
        'mode': mode
        }
    return render_template('rainmode.html',**gpiostate)
@app.route("/<act>")
def action(act):
    if act=="open":
        mode=1
        doorset(mode)
    elif act=="close":
        mode=0
        doorset(mode)
    gpiostate={
        'mode' :mode
        }
    return render_template('rainmode.html',**gpiostate)
 
if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)
