import grovepi
import grove6axis
import time

def getUltrasonicDist():
	# Read from Ultrasonic Ranger
	return grovepi.ultrasonicRead(2)

def getXAccel():
	# Read the X value from the Six Axis Accel/Magnetometer
	return grove6axis.getAccel()[1]

# SETUP GROVE PI #
# Connect Grove LED
grovepi.pinMode(3, "OUTPUT")
grovepi.pinMode(4, "OUTPUT")
# Initialise accelerometer
#grove6axis.init6Axis()

# INITIALISE VARIABLES #
# Get initial time to work out the program runtime
initialTime = time.time()

# SETUP CSV HEADER #
print("Raw Sensor Data\nTime, Current Distance (cm), Current X Acceleration (g)")

# RUN PROGRAM #
# Runs the program for a set amount of time in seconds (value can be changed if required)
while (time.time() - initialTime) < 30:
	# Output CSV values
	print("%f, %d, %f" % (time.time(), getUltrasonicDist(), getXAccel()))