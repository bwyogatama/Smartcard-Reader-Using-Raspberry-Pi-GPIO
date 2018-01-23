################################################
##    Created by:                             ##
##       -Bobbi Winema Yogatama               ##
##       -Dasi Edimas Akbar                   ##
##       -Rifqi Luthfan                       ##
##    Date: 12 January 2018                   ##
##    University: Institut Teknologi Bandung  ##
##    File Name: smartcardlib.py              ##
##    Description:                            ##
################################################


## Import Libraries
import RPi.GPIO as GPIO
import wiringpi
import serial
import time
import termios
import re

VCC = 4
RST = 5
RX = 16
TX = 15
TRG = 6
INPUT=0
OUTPUT=1
LOW=0
HIGH=1
PUD_UP=2
PUD_OFF=0
Alt0 = 4


## Setup WiringPi
def init_setup():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(VCC,OUTPUT)
    wiringpi.pinMode(RST,OUTPUT)
    wiringpi.pinMode(TRG,INPUT)

## Activate cold reset
def cold_reset():
    wiringpi.digitalWrite(VCC,LOW)
    wiringpi.digitalWrite(RST,LOW)
    wiringpi.digitalWrite(VCC,HIGH)
    wiringpi.delayMicroseconds(5400)
    wiringpi.digitalWrite(RST,HIGH)

## Activate warm reset
def warm_reset():
    wiringpi.digitalWrite(RST,LOW)
    wiringpi.digitalWrite(VCC,HIGH)
    wiringpi.digitalWrite(RST,HIGH)
    wiringpi.digitalWrite(RST,LOW)
    wiringpi.delayMicroseconds(5400)
    wiringpi.digitalWrite(RST,HIGH)

## Read ATR Procedure
def read_ATR(serial):
    wiringpi.pinMode(TX,INPUT)
    wiringpi.pullUpDnControl(TX,PUD_UP)
    first = wiringpi.millis()

    data_str = ''
    while (wiringpi.millis()-first)<100:
        if wiringpi.serialDataAvail(serial)>0:
            first = wiringpi.millis()
            data = wiringpi.serialGetchar(serial)
            if (data<16):
                data *= 16
            data_str += ('{:02x}'.format(data)) + ' '

    wiringpi.pullUpDnControl(TX,PUD_OFF)
    wiringpi.pinModeAlt(TX,4)

    data_str = data_str.lstrip('00')
    return data_str

def read_response(serial,ser,length):
    wiringpi.pinMode(TX,INPUT)
    wiringpi.pullUpDnControl(TX,PUD_UP)

    first = wiringpi.millis()
    wiringpi.delay(50)

    ## Save all the data from RX excluding bounced data
    data_list = []
    num_ser = wiringpi.serialDataAvail(serial)
    while (wiringpi.millis()-first)<100:
        if wiringpi.serialDataAvail(serial)>0:
            first = wiringpi.millis()
            data = wiringpi.serialGetchar(serial)
            if (wiringpi.serialDataAvail(serial) < (num_ser-length)):
                data_list.append('{:02x}'.format(data))
    
    wiringpi.pullUpDnControl(TX,PUD_OFF)
    wiringpi.pinModeAlt(TX,4)
    return data_list

## Transmit APDU procedure
def transmit_APDU(apdu,serial,ser):
    apdulist=re.sub("[^\w]"," ",apdu).split()
    apdu_list=[]
    for x in apdulist:
        temp=chr(int(x,16))
        apdu_list.append(temp)

    response_list = []
    response_list2 = []
    if len(apdu_list)>5:
        for y in range(0,5):
            ser.write(apdu_list[y])
            print(""),
        response_list=(read_response(serial,ser,5))

        print("")
        print 'Response = ',
        for i in range(0,len(response_list)):
            print response_list[i],
        print

        for y in range(5,len(apdu_list)):
            ser.write(apdu_list[y])
            print(""),
        response_list2=(read_response(serial,ser,len(apdu_list)-5))

        print
        print 'Response = ',
        for i in range(0,len(response_list2)):
            print response_list2[i],
        print

        
    else:
        for y in apdu_list:
            ser.write(y)
            print(""),
        response_list=(read_response(serial,ser,len(apdu_list)))

        print
        print 'Response = ',
        for i in range(0,len(response_list)):
            print response_list[i],
        print
        
    print("")


