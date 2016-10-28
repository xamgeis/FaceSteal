import time
from multiprocessing import Process, Queue
from Servo import Servo

class CamControl:
		
	"""
	Servos are default to Servo X axis is assigned (servo-0) GPIO 4
		Servo Y axis is assigned (servo-0) GPIO 17
	"""
	def __init__(self):
		#ServoBlaster is what we use to control servo motors
		#Upper Limit for servos
		self._ServoXul = 250
		self._ServoYul = 230

		#Lower limit for servos
		self._ServoXll = 75
		self._ServoYll = 75

		self.servo_X = Servo(0, self._ServoXul, self._ServoXll) 
		self.servo_Y = Servo(1, self._ServoYul, self._ServoYll)

	def recenter( self, offset_x, offset_y ):
		#TODO
		print("Centering camera...")

	def camLeft(self, distance, speed):
		print "left"
		self.servo_X.moveClockwise(distance, speed)
		return;

	def camRight(self, distance, speed):
		print "right"
		self.servo_X.moveCounterClockwise(distance, speed)
		return;


	def camDown(self, distance, speed):
		print "down"
		self.servo_Y.moveCounterClockwise(distance, speed)
		return;


	def camUp(self, distance, speed):
		print "up"
		self.servo_Y.moveClockwise(distance, speed)
		return;
		
	"""
	Functions for tuning 
	"""
	def sweep(self):
		i = 0
		while True:
			try: 
				if i >= 180:
					step = -1
				elif i <= 0:
					step = 1
				self.servo_X.setDegree(i)
				self.servo_Y.setDegree(i)
				i = i + step

				time.sleep(0.01)
				self.servo_X.rest()
				self.servo_Y.rest()
			except KeyboardInterrupt:
				break
		print("\ntidying up")

"""
# For testing Implementation
if __name__ == "__main__":
	import time
	import CamControl
	print "Running"
	
	cam = CamControl.CamControl()
	cam.camLeft(20,1)
	cam.camUp(20,1)
"""
