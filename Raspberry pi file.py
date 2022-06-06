#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#MQTT PUBLISH

import paho.mqtt.publish as publish




#DHT11 libraries
import Adafruit_DHT
import time
#-------------------------



# Light sensor libraries
import smbus
import time
#-------------------------




# Ultrasonic sensor libraries
import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED

SPEED_OF_SOUND = 34000
MAX_DISTANCE= 50           # 10cm allowed since door remains closed all the time automatically (Assumption)

GPIO.setmode(GPIO.BCM)
TRIGGER = 23
ECHO = 24
#-------------------------

# Ultrasonic sensor setup
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
#-------------------------



#DHT11 setup-------------------
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
#-------------------------------




# -----light sensor-----------
BH1750_sensor = 0x23

received_add = 0x20

bus = smbus.SMBus(1)

def Light():
    address = bus.read_i2c_block_data(BH1750_sensor,received_add)
    val = Light_intensity(address)
    return val
    
def Light_intensity(address):
    result = (address[1] + (256 * address[0])) / 1.2  # proper conversion
    return (result)
#-------------------------------------------------------------------------





# Ultrasonic sensor distance function

def distance():
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    
    while (GPIO.input(ECHO) == 0):
        startTime= time.time()
        
    while (GPIO.input(ECHO) == 1):
        stopTime= time.time()
    
    timeElapsed = stopTime - startTime
    distance = timeElapsed * SPEED_OF_SOUND
    
    return distance

def sound_alarm():
    publish.single("alarm/status","on", hostname = "test.mosquito.org")



def Action():
    
    # set the 3 variables to false initially 
    bool exhaust = False
    bool temp_high = False
    bool door_open = False
     
    while True:
        
        # check light level------------------------------------------
        
        level = Light()  # read value of light
       # print(level)      # keep??
        

        if (level >= 1402):   # exhause is on
            exhaust = True
        else:
            exhaust = False
            
        #--------------------------------------------------------------

        
        # Temperature check----------------------------------------------------------------
        
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)  # read in temeperature
        
        # check whether temeperature is being printed -- extend to checking between range
        if humidity is not None and temperature is not None:  # valid values
            if(humidity  > 90) and (temperature > 50):        # not within range 
                temp_high = True
            else:
                temp_high = False
                
        else:
            temp_high = False

        #-----------------------------------------------------------------------------------   
            
        # ultrasonic sensor calculation-----------------------
        
        currentDistance = distance()
        print("Measured distance = %.2f cm" % currentDistance)
        
        if currentDistance > MAX_DISTANCE:
            door_open = True
        else:
            door_open = False
        
        #----------------------------------------------------
        
        # check conditions
        
        
        if (exhaust = False and temp_high = True and door_open = True):
            sound_alarm();
            
        time.sleep(5)
        
        
        
Action()

