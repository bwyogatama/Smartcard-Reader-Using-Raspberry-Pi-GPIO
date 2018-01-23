################################################
##    Created by:                             ##
##       -Bobbi Winema Yogatama               ##
##       -Dasi Edimas Akbar                   ##
##       -Rifqi Luthfan                       ##
##    Date: 12 January 2018                   ##
##    University: Institut Teknologi Bandung  ##
##    File Name: rpi_smartcard_reader.py      ##
##    Description:                            ##
################################################



from smartcardlib import init_setup, warm_reset, read_ATR, transmit_APDU
import termios
import serial
import wiringpi
import RPi.GPIO as GPIO
import time

VCC = 4
RST = 5
RX = 16
TX = 15
TRG = 6
TRG_wiringpi = 22
INPUT=0
OUTPUT=1
LOW=0
HIGH=1
PUD_UP=2
PUD_OFF=0
Alt0 = 4

        
        
def main():

    ## MAIN ALGORITHM

    ## Open Serial Port
    ser = serial.Serial (port='/dev/ttyAMA0',baudrate=9600,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_TWO,timeout=1)
    wiring_serial = wiringpi.serialOpen('/dev/ttyAMA0',9600)
    new = termios.tcgetattr(wiring_serial)
    new[2] |= termios.CSTOPB
    new[2] |= termios.PARENB
    termios.tcsetattr(wiring_serial,termios.TCSANOW,new)

    ## GUI
    print ('====================================================================')
    print ('            Xirka Silicon Technology Smart Card Reader              ')
    print ('====================================================================')
    print ('Instruction:')
    print ('1. Do not remove the smartcard in the middle of the program')
    print ('2. Enter x or X as APDU Command to exit the program')
    print ('3. Enter t or T as APDU Command to test the performance')
    print (' ')

    init_setup()
    warm_reset()


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRG, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    print 

    try:
        if wiringpi.digitalRead(TRG_wiringpi)==0:
            print "Waiting for Card";
            print
            GPIO.wait_for_edge(TRG, GPIO.RISING)
            ATR=read_ATR(wiring_serial)
            print "ATR :",ATR
            print 

            while True:
                apdu = raw_input("Enter APDU Command = ")
                if ((apdu == 'x') or (apdu == 'X')):
                    print
                    print "Please remove the smartcard..."
                    GPIO.wait_for_edge(TRG, GPIO.FALLING)
                    print
                    print "Thank you"
                    break
                elif (apdu=='t') or (apdu == 'T'):
                    start=time.time()
                    print
                    print ("Enter APDU Command = 00 a4 00 00 02 3f 00")
                    transmit_APDU('00 a4 00 00 02 3f 00',wiring_serial,ser)
                    print ("Enter APDU Command = 00 a4 00 00 02 30 00")
                    transmit_APDU('00 a4 00 00 02 30 00',wiring_serial,ser)
                    print ("Enter APDU Command = 00 a4 00 00 02 30 01")
                    transmit_APDU('00 a4 00 00 02 30 01',wiring_serial,ser)
                    print ("Enter APDU Command = 00 b0 00 00 08")
                    transmit_APDU('00 b0 00 00 08',wiring_serial,ser)
                    end = time.time()
                    print 'Execution time: ',(end - start), 'seconds'
                    break
                else:
                    transmit_APDU(apdu,wiring_serial,ser)
        else:
            ATR=read_ATR(wiring_serial)
            print "ATR :",ATR
            print 

            while True:
                apdu = raw_input("Enter APDU Command = ")
                if ((apdu == 'x') or (apdu == 'X')):
                    print
                    print "Please remove the smartcard..."
                    GPIO.wait_for_edge(TRG, GPIO.FALLING)
                    print
                    print "Thank you"
                    break
                elif (apdu=='t') or (apdu == 'T'):
                    start=time.time()
                    print
                    print ("Enter APDU Command = 00 a4 00 00 02 3f 00")
                    transmit_APDU('00 a4 00 00 02 3f 00',wiring_serial,ser)
                    print ("Enter APDU Command = 00 a4 00 00 02 30 00")
                    transmit_APDU('00 a4 00 00 02 30 00',wiring_serial,ser)
                    print ("Enter APDU Command = 00 a4 00 00 02 30 01")
                    transmit_APDU('00 a4 00 00 02 30 01',wiring_serial,ser)
                    print ("Enter APDU Command = 00 b0 00 00 08")
                    transmit_APDU('00 b0 00 00 08',wiring_serial,ser)
                    end = time.time()
                    print 'Execution time: ',(end - start), 'seconds'
                    break

                else:
                    transmit_APDU(apdu,wiring_serial,ser)            
    except KeyboardInterrupt:  
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    GPIO.cleanup()           # clean up GPIO on normal exit  


    wiringpi.serialClose(wiring_serial)
    ser.close()

if __name__=='__main__':
    main()
