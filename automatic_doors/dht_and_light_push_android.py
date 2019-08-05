
import threading
from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

dht_sensor_port = 7 # connect the DHt sensor to port 7
# use 0 for the blue-colored sensor and 1 for the white-colored sensor
light_sensor = 2 # port A1
dht_sensor_type = 0

light =0
temp =0
hum =0
cnt = 0
luandryCheck = 0
tcount = 0

dht_sensor_type = 0

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the$

setRGB(0,255,0)

class Recv_Message(threading.Thread):
    def run(self):

        host = '192.168.0.38'        # Symbolic name meaning all available inte$
        port = 12345     # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
 	    conn.sendall(data)
            print ("recv data : " + data)
            os.system("nodejs fcm-pushserver2.js r");
        conn.close()

communication = Recv_Message(name='recv')
communication.start()

def read_sensor():
        try:
                # pressure=pressure = bmp.readPressure()/100.0
                light=analogRead(light_sensor)
                therm_version =0
                [temp,humidity] = dht(dht_sensor_port,therm_version)   
                #Return -1 in case of bad temp/humidity sensor reading
                if isnan(temp) or isnan(humidity):              
                        return [-1,-1,-1]
                # return [pressure,light,temp,humidity]
                return [light,temp,humidity]

        #Return -1 in case of sensor error
        except (IOError,TypeError) as e:
                        return [-1,-1,-1]

while True:
        try:

                [light,temp,hum]=read_sensor()

                if(hum >= 40):
                    luandryCheck = 1

                if(hum <= 22):
                    if(luandryCheck == 1):
                        print("hum <= 22")
                        os.system("nodejs fcm-pushserver2.js h");
                        luandryCheck = 0

                if(temp > 24):
                    if(hum < 20 & tcount == 0):
                        print("temp > 24 and hum < 20")
                        os.system("nodejs fcm-pushserver2.js c");
                        tcount = 1

                # check if we have nans
                # if so, then raise a type error exception
                if isnan(temp) is True or isnan(hum) is True:
                        raise TypeError('nan error')

                t = str(temp)
                h = str(hum)
                l = str(light/10)

                cnt += 1
                setText("")

                if (cnt == 1):
                    setText_norefresh("Temp:" + t + "C\n" + "Humidity :" + h + "%")
                elif (cnt == 2):
                    setText_norefresh("Humidity :" + h + "%\n" + "Light :" + l)
                else :
                    setText_norefresh("Light :" + l +"\nTemp:" + t + "C")
                    cnt = 0

        except (IOError, TypeError) as e:
                print(str(e))
                # and since we got a type error
                # then reset the LCD's text
                setText("")

        except KeyboardInterrupt as e:
                print(str(e))
                # since we're exiting the program
                # it's better to leave the LCD with a blank text
                setText("")
                break

        # wait some time before re-updating the LCD
        sleep(2.0)



