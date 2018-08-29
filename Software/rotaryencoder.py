import RPi.GPIO as GPIO
from time import sleep
# setup GPIO options...
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class RotaryEnc:
    'Base Class for Rotary Encoder on the RPi GPIO Pins'
    
    def __init__(self,PinA,PinB,button,Position,REmin,REmax,inc):
        
        self.PinA = PinA                                        # GPIO Pin for encoder PinA
        self.PinB = PinB                                        # GPIO Pin for encoder PinB
        self.button = button                                    # GPIO Pin for encoder push button
        self.Position = Position                                # encoder 'position'
        self.min = REmin                                        # Max value
        self.max = REmax                                        # Min value
        self.inc = inc                                          # increment        
        self.old_button = 1                                     # start value for previous button state
        self.old_btn_rl = 1
        self.oldPinA = 1                                        # start value for previous PinA state
        self.button_release = 0                                 # initialise outputs
        self.button_down = 0                                    # initialise outputs        
        GPIO.setup(self.PinA, GPIO.IN)                          # setup IO bits...
        GPIO.setup(self.PinB, GPIO.IN)                          #
        GPIO.setup(self.button, GPIO.IN)                        #
                                                                #
    def read(self):                                             # Function to Read encoder...
        encoderPinA=GPIO.input(self.PinA)                       # get inputs...
        encoderPinB=GPIO.input(self.PinB)                       #
        if encoderPinA and not self.oldPinA:                    # Transition on PinA?
                if not encoderPinB:                             #    Yes: is PinB High?
                        self.Position=self.Position+self.inc    #        No - so we're going clockwise
                        if self.Position > self.max:            #        limit maximum value
                                self.Position = self.max        #
                                                                #
                else:                                           #
                                                                #           
                        self.Position=self.Position-self.inc    #        Yes - so we're going anti-clockwise
                        if self.Position < self.min:            #        limit minimum value
                                self.Position = self.min        #     
        self.oldPinA=encoderPinA                                #    No: just save current PinA state for next time        
                                                                #
    def read_button(self):                                      # Function to Read encoder button...
        button=GPIO.input(self.button)                          # get input...
        #print(str(button))
        if button and  not self.old_button:                      # 'Upward' transition on button?
            self.button_release=1                               #      Yes - so set release output
        else:                                                   #    
            self.button_release=0                               #      No - so clear it
        if not button and self.old_button:                      # 'Downward' transition on button?
            self.button_down = 1                                #       Yes - so set 'down' button
        else:                                                   #                                                
            self.button_down = 0                                #       No - so clear it
        self.old_button=button 
