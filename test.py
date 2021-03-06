# This is a simple test of the Lidar.  It isn't threaded.


from lidar_lite import Lidar_Lite
import time

from collections import deque

lidar = Lidar_Lite()
connected = lidar.connect(1)


if connected < -1:
  print "Not Connected"
  timpe.sleep(1)
  connected = lidar.connect(1)

# Found it necessary to try connect twice ocasionally.
if connected < -1:
  print "Still not connected!"
else:
  print "Connected"

lidar.writeAndWait( 0x04, 0x0A )
lidar.writeAndWait( 0x11, 0x0A ) # Distance measurements per request.  Using 10.


xRange = []
maxItemsInQueue = 10
measurements = deque(xRange, maxItemsInQueue)

try:
  doContinue = True

  while doContinue:

    distanceCM = lidar.getDistance()
    distanceInch = distanceCM / 2.54
#    print "Inches:  ", distanceInch

    measurements.appendleft( distanceInch )
    sumOfMeasurements = sum( measurements )
    average = sumOfMeasurements / len( measurements )
    print 'RA: {:.2f}'.format(average)

# Haven't worked on Velocity.
    velocityMetersPerSecond = lidar.getVelocity()
    velocityInchesPerSecond = velocityMetersPerSecond / 39.3700787
    velocityInchesPerMinute = velocityInchesPerSecond * 60
 
    #print "Inches per minute: ", velocityInchesPerMinute 

    time.sleep(1)

except KeyboardInterrupt:
  print " "

print "Bye!"
