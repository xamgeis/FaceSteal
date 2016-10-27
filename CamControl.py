import time
from multiprocessing import Process, Queue

class CamControl:
	#Upper Limit for servos
	_ServoXul = 250
	_ServoYul = 230

	#Lower limit for servos
	_ServoXll = 75
	_ServoYll = 75
		
	"""
	Servos are default to Servo X axis is assigned (servo-0) GPIO 4
		Servo Y axis is assigned (servo-0) GPIO 17
	"""
	def __init__(self):
		#ServoBlaster is what we use to control servo motors
		self.servoBlaster = open('/dev/servoblaster', 'w')
		"""
		self.servo_X = Servo(pi, servoX_pin) 
		self.servo_Y = Servo(pi, servoY_pin)
		"""
		self.ServoXcp = Queue()	
		self.ServoXdp = Queue()	
		self.ServoXs  = Queue()	
		self.ServoYcp = Queue()	
		self.ServoYdp = Queue()	
		self.ServoYs  = Queue()

		self._ServoXcp = 99
		self._ServoXdp = 100
		
		self._ServoYcp = 99
		self._ServoYdp = 100

	def recenter( self, offset_x, offset_y ):
		#TODO
		print("Centering camera...")

	def camRight(self, distance, speed):
		print "right"
		if not self.ServoXcp.empty():
			self._ServoXcp = self.ServoXcp.get()
		self._ServoXdp = self._ServoXcp + distance
		if self._ServoXdp > CamControl._ServoXul:
			self._ServoXdp = CamControl._ServoXul
		self.ServoXdp.put(self._ServoXdp)
		self.ServoXs.put(speed)
		return;

	def camLeft(self, distance, speed):
		print "left"
		if not self.ServoXcp.empty():
			self._ServoXcp = self.ServoXcp.get()
		self._ServoXdp = self._ServoXcp - distance
		if self._ServoXdp < CamControl._ServoXul:
			self._ServoXdp = CamControl._ServoXul
		self.ServoXdp.put(self._ServoXdp)
		self.ServoXs.put(speed)
		return;


	def camUp(self, distance, speed):
		print "up"
		if not self.ServoYcp.empty():
			self._ServoYcp = self.ServoYcp.get()
		self._ServoYdp = self._ServoYcp + distance
		if self._ServoYdp > CamControl._ServoYul:
			self._ServoYdp = CamControl._ServoYul
		self.ServoYdp.put(self._ServoYdp)
		self.ServoYs.put(speed)
		return;


	def camDown(self, distance, speed):
		print "down"
		if not self.ServoYcp.empty():
			self._ServoYcp = self.ServoYcp.get()
		self._ServoYdp = self._ServoYcp - distance
		if self._ServoYdp < CamControl._ServoYul:
			self._ServoYdp = CamControl._ServoYul
		self.ServoYdp.put(self._ServoYdp)
		self.ServoYs.put(speed)
		return;



	# process X controls servoX	
	def PX(self):
		#set defaults
		speed = .1
		# make servo position unequal, so we know where the servo 
		# really is 
		self._ServoXcp = 99	
		self._SercoXdp = 100
		while True:
			time.sleep(speed)
			"""
			Constantly update self.ServoXcp in case the main process 
			needs to read it
			"""
			if self.ServoXcp.empty():
				self.ServoXcp.put(self._ServoXcp)

			# Constantly read self.ServoXdp in case the main process
			# has updated it
			if not self.ServoXdp.empty():
				self._ServoXdp = self.ServoXdp.get()

			# Constantly read self.ServoXs in case the main process 
			# has updated it with the higher speed value, the 
			# shorter the wait between loops will be, so the
			# servo moves faster
			if not self.ServoXs.empty():
				_ServoXs = self.ServoXs.get()
				speed = .1 / _ServoXs

			if self._ServoXcp < self._ServoXdp:
			 	self._ServoXcp += 1	#increment self.ServoXcp
			 	self.ServoXcp.put(self._ServoXcp) # move the servo a little bit
				self.servoBlaster.write('0=' + str(self._ServoXcp) + '\n')
				self.servoBlaster.flush() 
			elif self._ServoXcp > self._ServoXdp:
				self._ServoXcp -= 1  # decrement self.ServoXcp
				# move the servo a little bit
			 	self.ServoXcp.put(self._ServoXcp) # move the servo a little bit
				self.servoBlaster.write('0=' + str(self._ServoXcp) + '\n')
				self.servoBlaster.flush()

				# throw away the old self.ServoXcp value.
				if not self.ServoXcp.empty():
					trash = self.ServoXcp.get()
			elif self._ServoXcp == self._ServoXdp:
				_ServoXs = 1	# slow the speed; no need to eat CPU just waiting
	# process Y controls servoY	
	def PY(self):
		#set defaults
		speed = .1
		# make servo position unequal, so we know where the servo 
		# really is 
		self._ServoYcp = 99	
		_SercoYdp = 100
		while True:
			time.sleep(speed)
			"""
			Constantly update self.ServoYcp in case the main process 
			needs to read it
			"""
			if self.ServoYcp.empty():
				self.ServoYcp.put(self._ServoYcp)

			# Constantly read self.ServoYdp in case the main process
			# has updated it
			if not self.ServoYdp.empty():
				self._ServoYdp = self.ServoYdp.get()

			# Constantly read self.ServoYs in case the main process 
			# has updated it with the higher speed value, the 
			# shorter the wait between loops will be, so the
			# servo moves faster
			if not self.ServoYs.empty():
				_ServoYs = self.ServoYs.get()
				speed = .1 / _ServoYs

			if self._ServoYcp < self._ServoYdp:
			 	self._ServoYcp += 1	#increment self.ServoYcp
			 	self.ServoYcp.put(self._ServoYcp) # move the servo a little bit
				self.servoBlaster.write('1=' + str(self._ServoYcp) + '\n')
				self.servoBlaster.flush()
				
			
			elif self._ServoYcp > self._ServoYdp:
			 	self._ServoYcp -= 1  # decrement self.ServoYcp
				# move the servo a little bit
			 	self.ServoYcp.put(self._ServoYcp) # move the servo a little bit
				self.servoBlaster.write('1=' + str(self._ServoYcp) + '\n')
				self.servoBlaster.flush()

				# throw away the old self.ServoYcp value.
				if not self.ServoYcp.empty():
					trash = self.ServoYcp.get()
			elif self._ServoYcp == self._ServoYdp:
				_ServoYs = 1	# slow the speed; no need to eat CPU just waiting

			  	
	def run(self):
		# start subprocesses
		Process(target=self.PX, args=()).start()
		Process(target=self.PY, args=()).start()
		# wait for them to start
		time.sleep(1)
		
	"""
	Functions for tuning 
	"""
	def sweep_noSleep(self):
		self.pwm.set_pulse_start_in_micros(self.servo_Y.SERVO,0)		
		for i in range(500, 2501, 3):
			self.pwm.set_pulse_length_in_micros(self.servo_Y.SERVO, i)
			self.pwm.set_pulse_length_in_micros(self.servo_Y.SERVO, i)
			self.pwm.update()

	def moveTopRight(self):
		self.servo_X.setDegree(0)
		self.servo_Y.setDegree(180) 

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

		self.pi.stop()

	def moveX(self,degree):
		self.servo_X.setDegree(degree)
	
if __name__ == "__main__":
	import time
	import CamControl
	print "Running"
	
	cam = CamControl.CamControl()
	cam.run()
	cam.camRight(50,3)
	#cam.camLeft(20,3)
	cam.camUp(50,3)
	#cam.camDown(20,3)

	print "stop"
