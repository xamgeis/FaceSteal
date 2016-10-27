import pigpio 
class Servo:
	
	def __init__(self, pi, gpio_pin):
		self.pi = pi
		self.SERVO = gpio_pin
		self.MIN_WIDTH=500
		self.MAX_WIDTH=2500
		self.DEGREE = (self.MAX_WIDTH - self.MIN_WIDTH) / 180.0
		

	def setDegree ( self, degree ):
	        if degree >= 0 or degree <= 180:
	        	width = degree*self.DEGREE + self.MIN_WIDTH
	        	self.pi.set_servo_pulsewidth(self.SERVO, width)

	def setMinWidth( self,min_width ):
		self.MIN_WIDTH = min_width

	def setMaxWidth (self,max_width):
		self.MAX_WIDTH = max_width
	
	def rest (self):
		self.pi.set_servo_pulsewidth(self.SERVO, 0)
