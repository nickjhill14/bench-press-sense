import grovepi
import grove6axis
import time
# MEDIAN FILTERING IMPORT #
import collections

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
# Get initial time to work out the program runtime (60 seconds)
initialTime = time.time()
# MEDIAN FILTERING
# Create a deque for history (double-ended list)
historyBuffer = collections.deque(maxlen = 21)
# HIGH PASS FILTERING #
filterOut = 0
# Change to increase/decrease the filter's effectiveness
constant = 0.5
lastValue = 0

# SETUP CSV HEADER #
print("Filtered Sensor Data\nTime, Current Distance (cm), Median, Raw Current X Acceleration(g), Filtered Current X Acceleration (g)")

# RUN PROGRAM #
# Runs the program for a set amount of time in seconds (value can be changed if required)
while (time.time() - initialTime) < 60:
	# MEDIAN FILTERING #
	# Append to buffer
	historyBuffer.append(getUltrasonicDist())
	# Sort the buffer
	orderedHistory = sorted(historyBuffer)
	# Get the median value of the buffer
	median = orderedHistory[int(len(orderedHistory) / 2)]

	# HIGH PASS FILTERING #
	value = getXAccel()
	# First order high pass formula
	filterOut = constant * (filterOut + value - lastValue)
	# Save current value for use in the next iteration
	lastValue = value

	# Output CSV values
	print("%f, %d, %d, %f, %f" % (time.time(), getUltrasonicDist(), median, getXAccel(), filterOut))