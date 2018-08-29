#!/usr/bin/python
import time
from time import sleep
#from RPi import GPIO
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import untangle
import rotaryencoder as Renc

import spidev
import os
import math


#Import/Parsing Profiles.xml
obj = untangle.parse("profiles.xml")

# Raspberry Pi pin configuration:



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(25, GPIO.OUT)
#GPIO.output(25, GPIO.HIGH)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#clkLastState = GPIO.input(clk)
#stage = 0

# BeagleBone Black configuration:
# lcd_rs        = 'P8_8'
# lcd_en        = 'P8_10'
# lcd_d4        = 'P8_18'
# lcd_d5        = 'P8_16'
# lcd_d6        = 'P8_14'
#

Position = 0

lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 12
lcd_backlight = 4
        
lcd_columns = 16
lcd_rows    = 2

global stage
stage=0


#---Motor Pins

in1 = 24
in2 = 23
en = 25
#Setup Motor pins

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)

class Display:
    'Base Class for all Display operations'
    def __init__(self):
        print("Fuck you")
           
    def boot(self):
        print ("Fuck all")
        self.msg1 = "<    Re        >"
        self.msg2 = "\n<      Print   >"
        for i in range(len(self.msg1)):
            lcd.clear()
            lcd.message(self.msg1[:i+1])
            time.sleep(0.1)	
        for i in range(len(self.msg2)):
            lcd.clear()
            lcd.message(self.msg1 + self.msg2[:i+1])
            time.sleep(0.1)
        #time.sleep(4)
            time.sleep(0.01)
        return
    
    # Function to read SPI data from MCP3008 chip
    # Channel must be an integer 0-7
    def ReadChannel(self, channel):
      self.adc = spi.xfer2([1,(8+channel)<<4,0])
      self.data = ((self.adc[1]&3) << 8) + self.adc[2]
      return self.data
     
    # Function to convert data to voltage level,
    # rounded to specified number of decimal places.
    def ConvertVolts(self, data):
      self.volts = (data * 3.3) / float(1023)
      self.volts = round(self.volts,2)
      return self.volts
     
    # Function to calculate temperature from
    # TMP36 data, rounded to specified
    # number of decimal places.
    def steinhart_temperature_C(self,rv, To=25.0, beta=3950.0):
        self.Ro=100000.0
        self.steinhart = math.log(rv / self.Ro) / beta      # log(R/Ro) / beta
        self.steinhart += 1.0 / (To + 273.15  )     # log(R/Ro) / beta + 1/To
        self.steinhart = (1.0 / self.steinhart) - 273.15   # Invert, convert to C
        
        return self.steinhart
    
    def ConvertTemp(self, data):
     
      # ADC Value
      self.d = data
      R = 100000/(float(1023)/self.d-1)
      #R = 80105.6338
      print(R)
      Tm= self.steinhart_temperature_C(R)
      
      return Tm
    
    def stage0(self):
        print("HOME")
        lcd.clear()
        lcd.show_cursor(True)
        lcd.blink(True)

        lcd.message('+Start Recycling\n*Profiles')
        lcd.set_cursor(0,0)
        self.x0 = 0
        self.stage= 0
        self.Position=0
                #lcd_message('Recycle')
                #lcd_send_byte(LCD_LINE_2, LCD_CMD)
                #lcd_message("Profiles")
        while self.stage == 0:                 
                        RE.read()   
                        if self.Position != RE.Position:
                            self.Position = RE.Position
                            if(self.x0==0):
                                self.x0=1
                                lcd.set_cursor(0,1)
                            elif(self.x0==1):
                                self.x0=0
                                lcd.set_cursor(0,0)
                                    #else:
                                     #   x0=1
                                      #  x1=0
                                       # lcd.set_cursor(0,0)
                        RE.read_button()                                             # Yes: so print a message
                        if RE.button_release:                                      # Has it been released
                            if(self.x0== 0):
                                self.stage = 1
                                lcd.clear()
                                lcd.show_cursor(True)
                                lcd.blink(True)

                                lcd.message('+PLA\n+ABS          <-')
                                lcd.set_cursor(0,0)
                                self.stage1(self.stage)
                                
                            elif(self.x0==1):
                                self.stage = 2
                                lcd.clear()
                                lcd.show_cursor(True)
                                lcd.blink(True)

                                lcd.message('+PLA\n*ABS          <-')
                                lcd.set_cursor(0,0)
                                self.stage2(self.stage)
                                
                            else:
                                lcd.set_cursor(0,0)
                                self.x0 = 0
        #return stage;
    def stage1(self,stage):
        self.x1_1 = 0
        self.stage =stage
        lcd.set_cursor(0,0)
        self.Position = 0
        while self.stage == 1:
                RE.read()   
                if self.Position != RE.Position:
                    self.Position = RE.Position
                    if(self.x1_1==0):
                        self.x1_1=1
                        lcd.set_cursor(0,1)
                    elif(self.x1_1 == 1):
                        self.x1_1=2
                        lcd.set_cursor(15,1)
                    elif(self.x1_1 == 2):
                        self.x1_1=0
                        lcd.set_cursor(0,0)
                    #else:
                        #self.x2_1 = 1
                        #lcd.set_cursor(0,0)
                             #   x0=1
                              #  x1=0
                               # lcd.set_cursor(0,0)
                RE.read_button()                                             # Yes: so print a message
                if RE.button_release:                                      # Has it been released
                    if(self.x1_1 == 0):
                        self.f=1
                    elif(self.x1_1==2):
                         return self.stage0()
                    elif(self.x1_1==1):
                        self.f =2
                    else:
                        lcd.set_cursor(0,0)
                        x2_1=0
                
                    lcd.clear()
                    lcd.show_cursor(True)
                    lcd.blink(True)
                    self.msg='Duration:   min'
                    lcd.message(self.msg)
                    lcd.set_cursor(10,0)
                    self.stage = 1.21
                    self.stage1_2(self.stage,self.f)
                    
    def stage1_2(self,stage,f):
        self.x1_2 = 0
        self.stage =stage
        self.f =f
        lcd.set_cursor(10,0)
        self.Position = 0
        RE.Position=0
        while self.stage == 1.21:
                RE.read()   
                if self.Position != RE.Position:
                    self.Position = RE.Position
                    if(self.Position < 0):
                        self.Position = 0
                        RE.Position= 0
                    lcd.clear()
                    lcd.show_cursor(True)
                    lcd.blink(True)
                    
                    lcd.message('Duration:'+str(self.Position)+' min')
                    lcd.set_cursor(10,0)
                    #else:
                        #self.x2_1 = 1
                        #lcd.set_cursor(0,0)
                             #   x0=1
                              #  x1=0
                               # lcd.set_cursor(0,0)
                RE.read_button()                                             # Yes: so print a message
                if RE.button_release:                                      # Has it been released
                    self.time = self.Position
                    
                    lcd.clear()
                    lcd.show_cursor(True)
                    lcd.blink(True)
                    self.msg=' Temp:  '+chr(223)+'C\n Time left:   min\n Cancel'
                    lcd.message(self.msg)
                    lcd.set_cursor(0,0)
                    self.stage = 12.1
                    self.stage1_21(self.stage,self.f,self.time)
    
    def stage1_21(self,stage,f,time):
        self.stage = stage
        self.f = f
        self.time = time
        self.x21_1=0
        self.Position = 0
        self.s = 0
        self.x12_1=0
        
        if(self.f ==1):
                    self.tempmin = obj.profiles.PLA['mintemp']
                    self.tempmax = obj.profiles.PLA['maxtemp']
                    self.speed= obj.profiles.PLA['speed']
        elif(self.f ==2):
                    self.tempmin = obj.profiles.ABS['mintemp']
                    self.tempmax = obj.profiles.ABS['maxtemp']
                    self.speed= obj.profiles.ABS['speed']
        else:
            lcd.clear()
            lcd.message('Error! Contact \nJogge!')
        #print(self.tempmin)
        #print(self.tempmax)
        GPIO.setup(2, GPIO.OUT)
        GPIO.output(2, GPIO.HIGH)
        while self.stage == 12.1 and self.time >0:
                if(self.s >= 60):
                    self.s = 1
                    sleep(0.998)
                    self.time = self.time -1
                    
                else:
                    sleep(0.998)
                    self.s = self.s +1
                print(self.time)
                print(self.s)
                
                
                
                # Define sensor channels
                self.temp_channel1  = 0
                self.temp_channel2  = 1
                self.temp_channel3  = 2
                self.temp_channel4  = 3
                 
                # Define delay between readings
                self.delay = 1
                 
                # Read the temperature sensor data 1
                self.temp_level1 = self.ReadChannel(self.temp_channel1)
                self.temp_volts1 = self.ConvertVolts(self.temp_level1)
                self.temp1       = self.ConvertTemp(self.temp_level1)
                  
                # Read the temperature sensor data 1
                self.temp_level2 = self.ReadChannel(self.temp_channel2)
                self.temp_volts2 = self.ConvertVolts(self.temp_level2)
                self.temp2       = self.ConvertTemp(self.temp_level2)
                  
                # Read the temperature sensor data 1
                self.temp_level3 = self.ReadChannel(self.temp_channel3)
                self.temp_volts3 = self.ConvertVolts(self.temp_level3)
                self.temp3      = self.ConvertTemp(self.temp_level3)
                  
                # Read the temperature sensor data 1
                self.temp_level4 = self.ReadChannel(self.temp_channel4)
                self.temp_volts4 = self.ConvertVolts(self.temp_level4)
                self.temp4       = self.ConvertTemp(self.temp_level4)
                 
                self.average = int((self.temp1 +self.temp2 + self.temp3 ))/ 3
                # Print out results
                print("--------------------------------------------")
                print("Temp : {} ({}V) {} deg C".format(self.temp_level1,self.temp_volts1,self.temp1))
                print("Temp : {} ({}V) {} deg C".format(self.temp_level2,self.temp_volts2,self.temp2))
                print("Temp : {} ({}V) {} deg C".format(self.temp_level3,self.temp_volts3,self.temp3))
                print("Temp : {} ({}V) {} deg C".format(self.temp_level4,self.temp_volts4,self.temp4))
                print(self.average)
                  #GPIO.setmode(GPIO.BOARD) # Set GPIO as numbering
                
                
                if( self.temp4 <= int(self.tempmin)):
                  GPIO.output(2, GPIO.HIGH)
                elif(self.temp4 >= int(self.tempmax)) :
                  GPIO.output(2, GPIO.LOW)
                else:
                    GPIO.output(2, GPIO.LOW)
                # Wait before repeating loop
                #time.sleep(delay)
                if(self.temp4 >= (int(self.tempmin)-10)):
                     GPIO.output(in1,GPIO.HIGH)
                     GPIO.output(in2,GPIO.LOW)
                     self.dut=(int(self.speed)*100)/9
                     p.ChangeDutyCycle(self.dut)
                
              
                RE.read()   
                if self.Position != RE.Position:
                    self.Position = RE.Position
                    #if(self.Position >= RE.Position):
                     #   if(self.x21_1 == 3):
                      #      self.x21_1 = 0
                       # else:
                        #    self.x21_1 = self.x21_1 + 1
                    #else:
                     #   if(self.x21_1==0):
                      #      self.x21_1 =3
                       # else:
                        #    self.x21_1 =- 1  also change number s x21_1
                    lcd.clear()
                    lcd.show_cursor(True)
                    lcd.blink(True)
                    if(self.x12_1==0):
                        self.x12_1=1
                        self.msg=' Temp:'+str(self.average)+chr(223)+'C\n Time left:'+str(self.time)+'min\n Cancel'
                        lcd.message(self.msg)
                        lcd.set_cursor(0,1)

                    elif(self.x12_1 == 1):
                        self.msg='Time left:'+str(self.time)+'min\nCancel'
                        lcd.message(self.msg)
                        lcd.set_cursor(0,0)
                        self.x12_1=2
                    elif(self.x12_1==2):
                        self.msg=' Time left:'+str(self.time)+'min\n Cancel'
                        lcd.message(self.msg)
                        lcd.set_cursor(0,1)
                        self.x12_1=3
                    elif(self.x12_1==3):
                        lcd.set_cursor(0,0)
                        self.x12_1=0
                        self.msg=' Temp:'+str(self.average)+chr(223)+'C\n Time left:'+str(self.time)+'min\n Cancel'
                        lcd.message(self.msg)
                else:
                    lcd.clear()
                    lcd.show_cursor(True)
                    lcd.blink(True)
                    if(self.x21_1==0):
                        self.msg=' Temp:'+str(self.average)+chr(223)+'C\n Time left:'+str(self.time)+'min\n Cancel'
                        lcd.message(self.msg)
                    elif(self.x21_1 == 1):
                        self.msg=' Time left:'+str(self.time)+'min\n Cancel'
                        lcd.message(self.msg)
                        lcd.set_cursor(0,0)
                    elif(self.x21_1==2):
                        self.x21_1=3
                        #lcd.set_cursor(0,1)
                    
                    lcd.message(self.msg)
                    
                            #else:
                             #   x0=1
                              #  x1=0
                               # lcd.set_cursor(0,0)
                    
                RE.read_button()                                             # Yes: so print a message
                if RE.button_release:                                      # Has it been released
                    if(self.x21_1 == 3):
                         GPIO.output(2, GPIO.LOW)
                         GPIO.output(in1,GPIO.LOW)
                         GPIO.output(in2,GPIO.LOW)
                         self.stage0()
                    else:
                        lcd.set_cursor(0,0)
                        
                        x1_1=0
                sleep(0.01)
        GPIO.output(2, GPIO.LOW)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        self.stage0()
    
    def stage2(self,stage):
        self.x2_1 = 0
        self.stage =stage
        lcd.set_cursor(0,0)
        self.Position = 0
        while self.stage == 2:
                RE.read()   
                if self.Position != RE.Position:
                    self.Position = RE.Position
                    if(self.x2_1==0):
                        self.x2_1=1
                        lcd.set_cursor(0,1)
                    elif(self.x2_1 == 1):
                        self.x2_1=2
                        lcd.set_cursor(15,1)
                    elif(self.x2_1 == 2):
                        self.x2_1=0
                        lcd.set_cursor(0,0)
                    #else:
                        #self.x2_1 = 1
                        #lcd.set_cursor(0,0)
                             #   x0=1
                              #  x1=0
                               # lcd.set_cursor(0,0)
                RE.read_button()                                             # Yes: so print a message
                if RE.button_release:                                      # Has it been released
                    if(self.x2_1 == 0):
                        lcd.clear()
                        lcd.show_cursor(True)
                        lcd.blink(True)
                        tempmin= obj.profiles.PLA['mintemp']
                        tempmax= obj.profiles.PLA['maxtemp']
                        speed= obj.profiles.PLA['speed']
                        self.msg=' Min. Temp.'+tempmin+'\n Max. Temp. '+tempmax+'\n Speed: '+speed
                        lcd.message(self.msg)
                        lcd.set_cursor(0,0)
                        self.stage = 2.1
                        self.f=1
                        self.stage2_1(self.stage,self.f)
                    elif(self.x2_1==2):
                         return self.stage0()
                    elif(self.x2_1==1):
                        lcd.clear()
                        lcd.show_cursor(True)
                        lcd.blink(True)
                        tempmin= obj.profiles.ABS['mintemp']
                        tempmax= obj.profiles.ABS['maxtemp']
                        speed= obj.profiles.ABS['speed']
                        msg=' Min. Temp.'+tempmin+'\n Max. Temp. '+tempmax+'\n Speed: '+speed
                        lcd.message(msg)
                        lcd.set_cursor(0,0)
                        self.stage = 2.1
                        self.f =2
                        self.stage2_1(self.stage,self.f)
                    else:
                        lcd.set_cursor(0,0)
                        x2_1=0
 
    def stage2_1(self,stage,f):
        self.stage = stage
        self.f = f
        self.x21_1=0
        self.Position = 0
        while self.stage == 2.1:
                RE.read()   
                if self.Position != RE.Position:
                    self.Position = RE.Position
                    #if(self.Position >= RE.Position):
                     #   if(self.x21_1 == 3):
                      #      self.x21_1 = 0
                       # else:
                        #    self.x21_1 = self.x21_1 + 1
                    #else:
                     #   if(self.x21_1==0):
                      #      self.x21_1 =3
                       # else:
                        #    self.x21_1 =- 1  also change number s x21_1
                    if(self.x21_1==0):
                        self.x21_1=1
                        lcd.clear()
                        lcd.show_cursor(True)
                        lcd.blink(True)
                        if(self.f == 1):
                            tempmin= obj.profiles.PLA['mintemp']
                            tempmax= obj.profiles.PLA['maxtemp']
                            speed= obj.profiles.PLA['speed']
                            self.msg=' Min. Temp.'+tempmin+'\n Max. Temp. '+tempmax
                            lcd.message(self.msg)
                        elif(self.f==2):
                            lcd.clear()
                            lcd.show_cursor(True)
                            lcd.blink(True)
                            tempmin= obj.profiles.ABS['mintemp']
                            tempmax= obj.profiles.ABS['maxtemp']
                            speed= obj.profiles.ABS['speed']
                            self.msg=' Min. Temp.'+tempmin+'\n Max. Temp. '+tempmax
                            lcd.message(self.msg)
                        lcd.set_cursor(0,1)
                    elif(self.x21_1 == 1):
                        self.x21_1=2
                        lcd.clear()
                        lcd.show_cursor(True)
                        lcd.blink(True)
                        if(self.f == 1):
                            tempmin= obj.profiles.PLA['mintemp']
                            tempmax= obj.profiles.PLA['maxtemp']
                            speed= obj.profiles.PLA['speed']
                            self.msg='Max. Temp. '+tempmax+'\n Speed: '+speed
                            lcd.message(self.msg)
                        elif(self.f==2):
                            lcd.clear()
                            lcd.show_cursor(True)
                            lcd.blink(True)
                            tempmin= obj.profiles.ABS['mintemp']
                            tempmax= obj.profiles.ABS['maxtemp']
                            speed= obj.profiles.ABS['speed']
                            self.msg='Max. Temp. '+tempmax+'\n Speed: '+speed
                            lcd.message(self.msg)
                        lcd.set_cursor(0,1)
                    elif(self.x21_1==2):
                        self.x21_1=3
                        lcd.clear()
                        lcd.show_cursor(True)
                        lcd.blink(True)
                        if(self.f == 1):
                            tempmin= obj.profiles.PLA['mintemp']
                            tempmax= obj.profiles.PLA['maxtemp']
                            speed= obj.profiles.PLA['speed']
                            self.msg='Speed: '+speed +'\n Home'
                            lcd.message(self.msg)
                        elif(self.f==2):
                            lcd.clear()
                            lcd.show_cursor(True)
                            lcd.blink(True)
                            tempmin= obj.profiles.ABS['mintemp']
                            tempmax= obj.profiles.ABS['maxtemp']
                            speed= obj.profiles.ABS['speed']
                            self.msg='Speed: '+speed +'\n Home'
                            lcd.message(self.msg)
                        lcd.set_cursor(0,1)
                    elif(self.x21_1 ==3):
                        self.x21_1=0
                        lcd.clear()
                        lcd.show_cursor(True)
                        lcd.blink(True)
                        if(self.f == 1):
                            tempmin= obj.profiles.PLA['mintemp']
                            tempmax= obj.profiles.PLA['maxtemp']
                            speed= obj.profiles.PLA['speed']
                            self.msg=' Min. Temp.'+tempmin+'\n Max. Temp. '+tempmax
                            lcd.message(self.msg)
                        elif(self.f==2):
                            lcd.clear()
                            lcd.show_cursor(True)
                            lcd.blink(True)
                            tempmin= obj.profiles.ABS['mintemp']
                            tempmax= obj.profiles.ABS['maxtemp']
                            speed= obj.profiles.ABS['speed']
                            self.msg=' Min. Temp.'+tempmin+'\n Max. Temp. '+tempmax
                            lcd.message(self.msg)
                        lcd.set_cursor(0,0)
                            #else:
                             #   x0=1
                              #  x1=0
                               # lcd.set_cursor(0,0)
                    
                RE.read_button()                                             # Yes: so print a message
                if RE.button_release:                                      # Has it been released
                    if(self.x21_1 == 3):
                        self.stage0()
                    else:
                        lcd.set_cursor(0,0)
                        x1_1=0
                sleep(0.01) 


# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


RE = Renc.RotaryEnc(4, 3,18,Position,-200,200,1)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000



D = Display()
#D.boot()

#print("here")   
D.stage0()
#print("now there")
        
        
        
        
    
