# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 18:07:38 2020

@author: Landen
"""
import time
import pyautogui
from random import randint, choice, uniform
from math import ceil


def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result)) 
    return result


    
def make_bezier(xys):

    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n - 1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                list(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier


def mouse_bez(init_pos, fin_pos, deviation, speed):
    '''
    GENERATE BEZIER CURVE POINTS
    Takes init_pos and fin_pos as a 2-tuple representing xy coordinates
        variation is a 2-tuple representing the
        max distance from fin_pos of control point for x and y respectively
        speed is an int multiplier for speed. The lower, the faster. 1 is fastest.
            
    '''

    #time parameter
    ts = [t/(speed * 100.0) for t in range(speed * 101)]
    
    #bezier centre control points between (deviation / 2) and (deviaion) of travel distance, plus or minus at random
    control_1 = (init_pos[0] + choice((-1, 1)) * abs(ceil(fin_pos[0]) - ceil(init_pos[0])) * 0.01 * randint(deviation / 2, deviation),
                init_pos[1] + choice((-1, 1)) * abs(ceil(fin_pos[1]) - ceil(init_pos[1])) * 0.01 * randint(deviation / 2, deviation)
                    )
    control_2 = (init_pos[0] + choice((-1, 1)) * abs(ceil(fin_pos[0]) - ceil(init_pos[0])) * 0.01 * randint(deviation / 2, deviation),
                init_pos[1] + choice((-1, 1)) * abs(ceil(fin_pos[1]) - ceil(init_pos[1])) * 0.01 * randint(deviation / 2, deviation)
                    )
        
    xys = [init_pos, control_1, control_2, fin_pos]
    bezier = make_bezier(xys)
    points = bezier(ts)

    return points
        

def connected_bez(coord_list, deviation, speed):

    '''
    Connects all the coords in coord_list with bezier curve
    and returns all the points in new curve
    
    ARGUMENT: DEVIATION (INT)
        deviation controls how straight the lines drawn my the cursor
        are. Zero deviation gives straight lines
        Accuracy is a percentage of the displacement of the mouse from point A to
        B, which is given as maximum control point deviation.
        Naturally, deviation of 10 (10%) gives maximum control point deviation
        of 10% of magnitude of displacement of mouse from point A to B, 
        and a minimum of 5% (deviation / 2)
    '''
    points = []
    j = 1
    
    
    while j < len(coord_list):
        points += mouse_bez(coord_list[j - 1], coord_list[j], deviation, speed)
        j += 1
    
    speed = 55 + randint(1,5)
    deviation = 2*randint(1,4)
    tweenseed = randint(1,3)
    pagspeed = 0
    
    
    #print("The current deviation is", deviation)
    #print("The current speed is", speed)
    
    
    if 0.5 < tweenseed < 1.5:
        for point in points:
            pyautogui.moveTo(*point,pagspeed, pyautogui.easeOutQuad)
            #pyautogui.moveTo(*point)
            #print(*point)
        #print("The current tween seed is easeOutQuad")
    if 1.5 < tweenseed < 2.5:
        for point in points:
            pyautogui.moveTo(*point,pagspeed, pyautogui.easeInBounce)
            #print(*point)
        #print("The current tween seed is easeInBounce")
    if 2.5 < tweenseed < 3.5:
        for point in points:
            pyautogui.moveTo(*point,pagspeed, pyautogui.easeInElastic)
            #print(*point)
        #print("The current tween seed is easeInElastic")

    
    
pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
pyautogui.PAUSE = 0  # Default: 0.1
initial = pyautogui.position()


speed = 55 + randint(0,5)
deviation = 2*randint(1,4)

sleeplower = 0.8
sleepupper = 0.9

'''
adjust the 4 parameters to vary sleep time, speed, and deviation on curves
'''

loop = 1
bigcounter = 0
counter = 0
while loop < 2:
      
    randcounter = randint(50,1200)  
    '''
    adjust this for relog scheme ^
   '''
    
    alchsperloop = 10
    '''
    adjust this for alchs per loop^
    '''
    
    breakvar = False
    for i in range(alchsperloop):
        print(bigcounter)
        
        initial = pyautogui.position()
        connected_bez((initial, (220, 220)), 0 ,speed) #clicks on banker
        time.sleep(uniform(0.4,0.6))
        pyautogui.click()
        time.sleep(uniform(1.2,1.5))
        
        initial = pyautogui.position()
        connected_bez((initial, (182, 122)), deviation ,speed) #clicks on ether
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (136, 120)), deviation ,speed) # clicks on bracelet
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (488, 47)), deviation ,speed) #exits bank window
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (584, 254)), deviation ,speed) # clicks on ether
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (629, 257)), deviation ,speed) # clicks on bracelet
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (750, 210)), deviation ,speed) # clicks on spell book
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (724, 337)), deviation ,speed) #clicks on highalch
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        thing = pyautogui.pixelMatchesColor(625, 250, (34, 30, 30), tolerance=1)
        
        if thing is True:
            
            initial = pyautogui.position()
            connected_bez((initial, (625, 254)), deviation ,speed) #alchs bracelet
            pyautogui.click()
            time.sleep(uniform(sleeplower,sleepupper))
            
            initial = pyautogui.position()
            connected_bez((initial, (650, 213)), deviation ,speed) #ckicks on inven
            pyautogui.click()
            time.sleep(uniform(sleeplower,sleepupper))
            
        else:
            breakvar = True
            break
        
        counter = counter + 1
        bigcounter = bigcounter + 1
        
        if counter is randcounter: #random relog function
            initial = pyautogui.position()
            connected_bez((initial, (650, 513)), deviation ,speed)#clicks on log out
            pyautogui.click()
            time.sleep(uniform(sleeplower,sleepupper))
            
            initial = pyautogui.position()
            connected_bez((initial, (655, 460)), deviation ,speed)#logs out
            pyautogui.click()
            time.sleep(uniform(sleeplower,sleepupper))
            
            time.sleep(uniform(600,1200))
            
            '''
            adjust how much time spent logged out^
            '''
            
            
            initial = pyautogui.position()
            connected_bez((initial, (470, 320)), deviation ,speed)#existing user
            pyautogui.click()
            time.sleep(uniform(sleeplower,sleepupper))
            
            initial = pyautogui.position()
            pyautogui.write('string', interval=0.25)
            time.sleep(uniform(sleeplower,sleepupper)) #types password
            
            initial = pyautogui.position()
            connected_bez((initial, (300, 350)), deviation ,speed)#log in
            pyautogui.click()
            time.sleep(uniform(8,10))
            
            initial = pyautogui.position()
            connected_bez((initial, (395, 362)), deviation ,speed)#click to play
            pyautogui.click()
            time.sleep(uniform(3,4))
    
        if bigcounter is randint(2000,2300):
            breakvar = True
            break
            '''
            can adjust how after how many alchs to log out
            '''
    if breakvar is True:
        print("break")
        break
        
    
    for i in range(1):
        #start GE
        initial = pyautogui.position()
        connected_bez((initial, (40, 300)), deviation ,speed) # clicks on ge guy
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (58, 169)), deviation ,speed) # clicks on buy option
        pyautogui.click()
        time.sleep(1.2)
        
        pyautogui.write('ether', interval=0.25)
        time.sleep(uniform(1,1.2)) #types ether into search
        
        initial = pyautogui.position()
        connected_bez((initial, (80, 410)), deviation ,speed) # clicks on ether bracelet
        pyautogui.click()
        time.sleep(1.2)
        
        initial = pyautogui.position()
        connected_bez((initial, (115, 236)), deviation ,speed) # clicks on buy 100, now 10 
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (448, 238)), deviation ,speed) # clicks on 5% thing
        pyautogui.click(clicks=2)
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (264, 314)), deviation ,speed)# clicks on confirm
        pyautogui.click()
        time.sleep(uniform(2,3))
        
        initial = pyautogui.position()
        connected_bez((initial, (455, 95)), deviation ,speed)# clickcs on collect
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (484, 63)), deviation ,speed)# exits ge window
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (220, 220)), 0 ,speed)#click on banker
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (585, 260)), deviation ,speed)#right click on bracelets
        pyautogui.click(button='right')
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (573, 361)), deviation ,speed)#clicks on dep all
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
        
        initial = pyautogui.position()
        connected_bez((initial, (488, 47)), deviation ,speed)#exits bank window
        pyautogui.click()
        time.sleep(uniform(sleeplower,sleepupper))
    
    









