#
# 9/18/2017
# 0.0.3 SPECIAL LIDAR working
#
# September 27, 2017
# 0.1.5 Moving average working
#
# September 27, 2017
# 0.1.6 Minor changes
#
# September 27, 2017
# 0.1.7 File name changed
#
# September 30, 2017
# 0.1.8 Added thread.  There is an infinite loop.
#
# September 30, 2017
# 0.1.9 Fixed infinite loop.
#
# October 1, 2017
# 0.1.10 Merging code into thread
#
# October 1, 2017
# 0.1.11 Attribute error
#
# October 2, 2017
# 0.1.12 WORKS - NOT
#
# October 3, 2017
# 0.1.13 Added call to Lidar_Lite.__init__()
# Now it works
#
# October 3, 2017
# 0.1.14 Merging code into thread
#
# October 3, 2017
# 0.1.15 deleted extraneous code in LidarLiteClass
#
# October 3, 2017
# 0.2.16 Major shift to threeading.  Can't do a <control>-c to stop
#
# October 3, 2017
# 0.2.17 Infinite loop fixed.
#
# October 3, 2017
# 0.2.18 Done!!!
#
# October 15, 2017
# 0.2.19 Improved accuracy.
#
#
#  Merge into other code
#


from threading import Thread
import time



from lidar_lite import Lidar_Lite
import time

from collections import deque




class LidarLiteChild(Lidar_Lite):
  'LidarLiteChild documentation'

  def __init__(self):
    super( LidarLiteChild, self ).__init__()
    print "LidarLiteChild constructor"
    self._running = True

  def terminate(self):
    self._running = False
  
  def run(self):
    xRange = []
    maxItemsInQueue = 10
    measurements = deque(xRange, maxItemsInQueue)

    while self._running:

      distanceCM = self.getDistance()
      distanceInch = distanceCM / 2.54
#        print "Inches:  ", distanceInch

      measurements.appendleft( distanceInch )
      sumOfMeasurements = sum( measurements )
      average = sumOfMeasurements / len( measurements )
      print 'Running average Inches: {:.2f}'.format(average)


#    velocityMetersPerSecond = lidar.getVelocity()
#    velocityInchesPerSecond = velocityMetersPerSecond / 39.3700787
#    velocityInchesPerMinute = velocityInchesPerSecond * 60
 
    #print "Inches per minute: ", velocityInchesPerMinute 

      time.sleep(1)




#Create Class
lidarLiteChild = LidarLiteChild()

connected = lidarLiteChild.connect(1)

#print "Connected = ", connected

if connected >= 0:  #TODO Is this value correct???
  print "Connected"

  lidarLiteChild.writeAndWait( 0x04, 0x0A )
  lidarLiteChild.writeAndWait( 0x11, 0x0A ) # Distance measurements per request.  Using 10.
  lidarLiteChild.writeAndWait( 0x1C, 0x60 ) # Reduce sensitivity and errors per manual.

  #Create Thread
  lidarLiteChildThread = Thread(target=lidarLiteChild.run)

  #Start Thread
  lidarLiteChildThread.start()

  time.sleep(120)

  lidarLiteChild.terminate()
  print "Thread finished"

else:
  print "Not Connected"

