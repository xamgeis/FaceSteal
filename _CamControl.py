import time
from multiprocessing import Process, Queue

class CamControl:
    def __init__(self, servoX_pin, servoY_pin):
#ServoBlaster is what we use to control servo motors
        ServoBlaster = open('/dev/servoblaster', 'w')
        """
        self.servo_X = Servo(pi, servoX_pin) 
        self.servo_Y = Servo(pi, servoY_pin)
        """
        # start subprocesses
        Process(PX, args=()).start()
        Process(PY, args=()).start()
            # wait for them to start
        time.sleep(1)
	

	def recenter( self, offset_x, offset_y ):
		#TODO
		print("Centering camera...")

	def camRight(self):
		#TODO
		print "left"

	def camLeft(self):
		print "right"

	def camUp(self):
		print "up"

	def camDown(self):
		print "down"

	# process X controls servoX	
	def PX():
		#set defaults
		speed = .1
		# make servo position unequal, so we know where the servo 
		# really is 
		_ServoXcp = 99	
		_SercoXdp = 100
		while True:
			time.sleep(speed)
			"""
			Constantly update ServoXCP in case the main process 
			needs to read it
			"""
			if ServoXcp.empty():
				ServoXcp.put(_ServoXcp)

			# Constantly read ServoXDP in case the main process
			# has updated it
			if not ServoXdp.empty():
				_ServoXdp = ServoXdp.get()

			# Constantly read ServoXS in case the main process 
			# has updated it with the higher speed value, the 
			# shorter the wait between loops will be, so the
			# servo moves faster
			if not ServoXs.empty():
				_ServoXs = ServoXs.get()
				speed = .1 / _ServoXs

			if _ServoXcp < _ServoXdp:
			 	_ServoXcp += 1	#increment ServoXcp
			 	ServoXcp.put(_ServoXcp) # move the servo a little bit
				ServoBlaster.write('0=' + str(_ServoXcp) + '\n')
				ServoBlaster.flush() 
			elif _ServoXcp > _ServoXdp:
				_ServoXcp -= 1  # decrement ServoXcp
				# move the servo a little bit
			 	ServoXcp.put(_ServoXcp) # move the servo a little bit
				ServoBlaster.write('0=' + str(_ServoXcp) + '\n')
				ServoBlaster.flush()

				# throw away the old ServoXcp value.
				if not ServoXcp.empty():
					trash = ServoXcp.get()
			elif _ServoXcp == _ServoXdp:
				_ServoXs = 1	# slow the speed; no need to eat CPU just waiting
	# process Y controls servoY	
	def PY():
		#set defaults
		speed = .1
		# make servo position unequal, so we know where the servo 
		# really is 
		_ServoYcp = 99	
		_SercoYdp = 100
		while True:
			time.sleep(speed)
			"""
			Constantly update ServoYCP in case the main process 
			needs to read it
			"""
			if ServoYcp.empty():
				ServoYcp.put(_ServoYcp)

			# Constantly read ServoYDP in case the main process
			# has updated it
			if not ServoYdp.empty():
				_ServoYdp = ServoYdp.get()

			# Constantly read ServoYS in case the main process 
			# has updated it with the higher speed value, the 
			# shorter the wait between loops will be, so the
			# servo moves faster
			if not ServoYs.empty():
				_ServoYs = ServoYs.get()
				speed = .1 / _ServoYs

			if _ServoYcp < _ServoYdp:
			 	_ServoYcp += 1	#increment ServoYcp
			 	ServoYcp.put(_ServoYcp) # move the servo a little bit
				ServoBlaster.write('0=' + str(_ServoYcp) + '\n')
				ServoBlaster.flush()
				
			
			elif _ServoYcp > _ServoYdp:
			 	_ServoYcp -= 1  # decrement ServoYcp
				# move the servo a little bit
			 	ServoYcp.put(_ServoYcp) # move the servo a little bit
				ServoBlaster.write('0=' + str(_ServoYcp) + '\n')
				ServoBlaster.flush()

				# throw away the old ServoYcp value.
				if not ServoYcp.empty():
					trash = ServoYcp.get()
			elif _ServoYcp == _ServoYdp:
				_ServoYs = 1	# slow the speed; no need to eat CPU just waiting



			  	

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

	print "Running"

	print "stop"
