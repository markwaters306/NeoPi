'''
    NeoPixel Ring Class
'''

import time
import board
import neopixel
import numpy as np
import math

class Colour():
    def __init__(self,g,r,b):
        self.r = r
        self.g = g
        self.b = b
        self.rgb = [r,g,b]

class NeoRing():
    def __init__(self, no_leds, strip):
        self.no_leds = no_leds
        self.strip = strip
        self.leds = np.ones((3,self.no_leds))

    def Linear_Move(self, a_current, a_target,no_of_steps=10):
        '''
        Given the current colour array and a target colour array,
        calculate the steps that needs to be taken to move linearly
        from one colour to another
        '''
        diff = a_target - a_current
        step_size = diff / no_of_steps
        steps = []
        for i in range(0, no_of_steps):
            step = (a_current + (step_size * i)).astype(int)
            steps.append(step)
        steps.append(a_target.astype(int))

        return(steps)

    def Drip_Drop(user_colour, wait_ms=50,no_of_leds=3,no_of_steps=10):
        '''
        This function will take a make a random selection of leds max bright and then
        fade down to the base brightness
        This function is called no_of_steps times + 1 (default = 10 + 1 = 11)
        '''

        # Set the led array to the given colour
        self.leds[0,:] = user_colour.g
        self.leds[1,:] = user_colour.r 
        self.leds[2,:] = user_colour.b 

        # Select random leds
        rand_leds = np.random.randint(1,24,no_of_leds) #should be 0,24 but it doesn't like 0 for some raison

        #In order to make any given colour brighter
        # it is necessary to work out the ratio of colour
        ratio = self.leds[:,0]/leds[:,0].max()
        full_brightness = ratio * 255

        # Show the Leds
        Show_Led_Array(self.leds)

        # set the random leds to full brightness
        for i in range(0,self.no_of_leds):
            self.leds[:,rand_leds[i]] = full_brightness
        # get the list of steps to drop them down to the orginal brightness
        a_target = self.leds[:,0]
        steps = Linear_Move(full_brightness,a_target,no_of_steps=no_of_steps)

        # Display the steps on the led ring
        for step in steps:
            # set the random leds to step value
            for i in range(0,self.no_of_leds):
                self.leds[:,rand_leds[i]] = step
            self.Show_Led_Array()
            time.sleep(wait_ms/1000)

    def Noise(user_colour, strength_p=0.3, wait_ms=50):
        '''
        Take a given colour and generate a radnom array of size 24
        add the noise to the colour and then show
        This function will call led show only once
        '''
        rand_noise = np.random.rand(24)
        self.leds[0,:] = user_colour.g
        self.leds[1,:] = user_colour.r 
        self.leds[2,:] = user_colour.b 

        leds = leds + (leds * (rand_noise - 0.5) * strength_p)
        Show_Led_Array()
        sleep(wait_ms/1000)

    def Show_Led_Array(self):
        '''
        Set the entire wheel to the data stored in leds array
        '''
        for i in range(0,self.no_leds):
            self.strip[i] = self.leds[:,i]
            strip.show()

    def color_wipe(self, strip, colour, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            # self.strip.setPixelColor(i, color)
            self.strip[i] = colour.rgb
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def blockColour(self, colour):
        '''
        Set the entire wheel to one colour
        '''
        for i in range(self.no_leds):
            #strip.setPixelColor(i, colour)
            self.strip[i] = colour.rgb
            self.strip.show()
            time.sleep(100/1000)
    
    def Breathing_Colour(self, colour, wait_ms=75,steps=100,depth_p = 0.5):
        '''
        Take a given colour and fade up and down
        '''
        #Calculte the depth per colour
        depth_g = int(colour.g * depth_p)
        depth_r = int(colour.r * depth_p)
        depth_b = int(colour.b * depth_p)

        # loop over a sin wave
        for i in range(0,360):
            #calc new colour value
            g_new = int(colour.g + (depth_g * math.sin(i * (math.pi/180))))
            r_new = int(colour.r + (depth_r * math.sin(i * (math.pi/180))))
            b_new = int(colour.b + (depth_b * math.sin(i * (math.pi/180))))

            for j in range(strip.numPixels()):
                strip[j] = [r_new, g_new, b_new]
            strip.show()
            time.sleep(wait_ms/1000)

    def Spin(self, user_colour, strength_p=0.3,wait_ms=1):
    '''
    Take a give colour, generate a sin wave across 24 points and multiply the orginal colour
    Then on each step move the sin wave in phase across each led creating a bright spining spot
    This function will call led show 24 times
    '''
        c = self.leds.shape[1]

        # for each step rotatate the spin by 1 degree
        sin_wave = np.sin(np.array(np.linspace(0,360,180) * np.pi / 180. ))
        for i in range(180):
            indices = np.arange(24) * 8 + i
            sin_wave_chunk = sin_wave.take(indices,mode='wrap')
            for j in range(0,24):
                new_g = user_colour.g + (user_colour.g * sin_wave_chunk[j] *strength_p)
                new_r = user_colour.r + (user_colour.r * sin_wave_chunk[j] *strength_p)
                new_b = user_colour.b + (user_colour.b * sin_wave_chunk[j] *strength_p)
                leds[0,j] = new_g if new_g <= 255 else 255
                leds[1,j] = new_r if new_r <= 255 else 255
                leds[2,j] = new_b if new_b <= 255 else 255
                leds[0,j] = new_g if new_g >= 0 else 0
                leds[1,j] = new_r if new_r >= 0 else 0
                leds[2,j] = new_b if new_b >= 0 else 0
            Show_Led_Array(self.leds)
            time.sleep(wait_ms/1000)