#!/usr/bin/python

import RPi.GPIO as GPIO

f=open('/dev/snd/midiC0D0') #Opens the USB MIDI gadget for reading incoming MIDI messeges. Run 'ls /dev/snd/' to discover your correct MIDI device

LED1 = 21 #Assign LED1 to Pin 21
LED2 = 20 #Assign LED2 to Pin 20
LED3 = 16 #Assign LED3 to Pin 16

GPIO.setmode(GPIO.BCM) #Use the actual GPIO pin Number instead of board pin numbers

GPIO.setwarnings(False) #Ignore GPIO warnings

GPIO.setup(LED1,GPIO.OUT) #Set LED1 as an output
GPIO.setup(LED2,GPIO.OUT) #Set LED2 as an output
GPIO.setup(LED3,GPIO.OUT) #Set LED3 as an output

pwm1 = GPIO.PWM(LED1,1000) #Create a PWM instance on LED1 with a polling rate of 1000Hz
pwm2 = GPIO.PWM(LED2,1000) #Create a PWM instance on LED2 with a polling rate of 1000Hz
pwm3 = GPIO.PWM(LED3,1000) #Create a PWM instance on LED3 with a polling rate of 1000Hz

pwm1.start(0) #Start PWM Output
pwm2.start(0) #Start PWM Output
pwm3.start(0) #Start PWM Output

while True:
        bytes = f.read(3) #Read the first three bytes of any incoming MIDI messeges

        if bytes[0] == '\x90': #If MIDI note is ON, \x90, then...
                note = (ord(bytes[1])) #Set variable 'note' to a numeric note value from the MIDI messege
                vel = (ord(bytes[2])) #Set variable 'vel' to a numeric velocity value from the MIDI messege
                bright = int(vel)/127.0*100.0 #Convert the velocity range from 1-127 to 1-100 for PWM, and assign it to variable 'bright'

                print'Note : ',note #Print current MIDI note
                print'Velocity : ',vel #Print current MIDI velocity
                print'Brightness : ',bright #Print current PWM brightness

                if note == 60: #60 is the numeric value for middle C
                        pwm1.ChangeDutyCycle(bright) #Assign LED1 PWM to the current brightness level assigned by the MIDI velocity
                if note == 62: #62 is the numeric value for the D above middle C
                        pwm2.ChangeDutyCycle(bright) #Assign LED2 PWM to the current brightness level assigned by the MIDI velocity
                if note == 64: #62 is the numeric value for the E above middle C
                        pwm3.ChangeDutyCycle(bright) #Assign LED3 PWM to the current brightness level assigned by the MIDI velocity

        elif bytes[0] == '\x80': #If MIDI note is OFF, \x80, then...
                note = (ord(bytes[1]))

                if note == 60:
                        pwm1.ChangeDutyCycle(0) #Assign LED1 PWM to 0 brightness
                if note == 62:
                        pwm2.ChangeDutyCycle(0) #Assign LED2 PWM to 0 brightness
                if note == 64:
                        pwm3.ChangeDutyCycle(0) #Assign LED3 PWM to 0 brightness

        else:
                print('Fail')
