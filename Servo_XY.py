from servo import Servo # this import returns no error
import time
from wavePWM import PWM
class Servos_xy:
	def __init__(self, pi, servoX_pin, servoY_pin):
		self.pi = pi
		self.servo_X = Servo(pi, servoX_pin) 
		self.servo_Y = Servo(pi, servoY_pin)

		self.pwm = PWM(pi)
		self.pwm.set_frequency(50)	# for servo

	def recenter( self, offset_x, offset_y ):
		#TODO
		print("Centering camera...")

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
	import pigpio
	import Servo_XY

	pi = pigpio.pi()

	if not pi.connected:
		exit(0)

	"""
	This code demonstrates using two servos controlling a camera on an 
	XY axis
	"""
	servos = Servo_XY.Servos_xy(pi, 18, 21)
	servos.moveTopRight()
#servos.sweep()

"""
	i = 0
	while True:
		try: 
			if i == 180:
				step = -1
			elif i == 0:
				step = 1

			servos.moveX(i)
			i = i + step
			time.sleep(0.1)
		except KeyboardInterrupt:
			pass
	print("\ntidying up")
	pi.stop()
"""
