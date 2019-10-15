import grovepi
import grove6axis
import time

# WHEN RUNNING THIS CODE IN THE EMULATOR THE ACC_Y VALUE IS THE VALUE TO CHANGE FOR THE X ACCELERATION (IGNORE THIS IF RUNNING THE SYSTEM IN REAL-LIFE)

def getUltrasonicDist():
	# Read from Ultrasonic Ranger
	return grovepi.ultrasonicRead(2)

def getXAccel():
	# Read the X value from the Six Axis Accel/Magnetometer
	return grove6axis.getAccel()[1]

def updateMinMaxDist(currentDist, minDist, maxDist):
	# Test if a new minimum or maximum distance has been found
	if currentDist < minDist:
		minDist = currentDist
	elif currentDist > maxDist:
		maxDist = currentDist
	return minDist, maxDist

def updateReps(currentDist, noOfReps, isRep):
	# Check that the distance is less than 10cm away
	if currentDist < 10 and not isRep:
		noOfReps += 1
		isRep = True
		# Send HIGH to switch on green LED
		grovepi.digitalWrite(4, 1)
	return noOfReps, isRep

def repCheck(currentDist, noOfReps, isRep):
	# Return true is the current distance is over 40cm away (does not check until the barbell is close to the body)
	if noOfReps == 0:
		return False
	elif currentDist > 40 and isRep:
		# Send LOW to switch off green LED
		grovepi.digitalWrite(4, 0)
		return False
	return isRep

def updateAvgAccelX(currentXAccel, timeDiff, totalXAccel):
	# Update the total amount of X acceleration
	totalXAccel += currentXAccel
	return totalXAccel / timeDiff, totalXAccel

def updateAvgSide(avgXAccel):
	# Returns the average side based on the X acceleration (positive is left and negative is right)
	if avgXAccel > 0.25:
		return "Left"
	elif avgXAccel < -0.25:
		return "Right"
	return "Center"

def updateRisk(currentDist, currentXAccel, avgXAccel):
	# If the current distance is far from the body and the current or average acceleration is high in either direction then send a warning
	if currentDist > 35 and abs(0 - currentXAccel) > 0.4 or abs(0 - avgXAccel) > 0.25:
		# Send HIGH to switch on the warning LED
		grovepi.digitalWrite(3, 1)
		return "High"
	# Send LOW to switch off the warning LED	
	grovepi.digitalWrite(3, 0)
	return "Low"

# SETUP GROVE PI #
# Connect Grove LED
grovepi.pinMode(3, "OUTPUT")
grovepi.pinMode(4, "OUTPUT")
# Initialise accelerometer (comment out if using the emulator)
grove6axis.init6Axis()

# INITIALISE VARIABLES #
# Get the initial time that the program starts running (approximately)
initialTime = time.time()
# Min and max distances have been set to the initial ultrasonic reading
minDist = getUltrasonicDist()
maxDist = getUltrasonicDist()
noOfReps = 0
# Checks if a rep has been made and then stays false until another rep is made to prevent continual increment of reps
isRep = False
# Used to find the average X acceleration
totalXAccel = 0
# HIGH PASS FILTERING VARIABLE INITIALISATION #
filterOut = 0
constant = 0.5
lastValue = 0

# SETUP CSV HEADER #
print("Feedback\nCurrent Distance (cm), Maximum Distance (cm), Minimum Distance (cm), No. of Reps, Average Side, Risk")

# RUN PROGRAM #
# Runs until manually terminated in the console using ctrl + c
while True:
	# Get sensor values
	currentDist = getUltrasonicDist()
	currentXAccel = getXAccel()

	# HIGH PASS FILTERING #
	# First order high pass formula
	filterOut = constant * (filterOut + currentXAccel - lastValue)
	# Save current value for use in the next iteration
	lastValue = currentXAccel

	# Check if a rep has been made
	isRep = repCheck(currentDist, noOfReps, isRep)

	# Update values
	minDist, maxDist = updateMinMaxDist(currentDist, minDist, maxDist)
	noOfReps, isRep = updateReps(currentDist, noOfReps, isRep)
	avgXAccel, totalXAccel = updateAvgAccelX(filterOut, time.time() - initialTime, totalXAccel)
	avgSide = updateAvgSide(avgXAccel)
	risk = updateRisk(currentDist, filterOut, avgXAccel)

	# Output CSV values
	print("%d, %d, %d, %d, %s, %s" % (currentDist, maxDist, minDist, noOfReps, avgSide, risk))

	# Pause as to not be overwhelmed with input
	time.sleep(0.25)