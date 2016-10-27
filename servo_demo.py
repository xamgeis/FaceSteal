#!/usr/bin/env python

#servo_demo.py

import sys
import time
import random
import pigpio

NUM_GPIO=32

MIN_WIDTH=1000
MAX_WIDTH=2000

step = [0]*NUM_GPIO
width = [0]*NUM_GPIO 
used =[False]*NUM_GPIO  

pi = pigpio.pi()

if not pi.connected:
	exit()

G = [18,21]	# servo 1 and 2 connected to gpio 18 & 21

for g in G:
	used[g] = True
	step[g] = 1
	width[g] = MIN_WIDTH 

print("Sending servos pulses to GPIO {}, control C to stop.".
		format(' '.join(str(g) for g in G)))

while True:
	
	try:
		
		for g in G:
			pi.set_servo_pulsewidth(g, width[g])

			print(g, width[g])
			width[g] += step[g]

			if width[g]<MIN_WIDTH or width[g]>MAX_WIDTH:
				step[g] = -step[g]
				width[g] += step[g]

			time.sleep(0.01)
	except KeyboardInterrupt:
		break
print("\nTidying up")

for g in G:
	pi.set_servo_pulsewidth(g,0)
pi.stop()
