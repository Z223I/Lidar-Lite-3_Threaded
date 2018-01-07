# This is the threaded version.


import time
from threading   import Thread
from lidar_lite  import Lidar_Lite
from collections import deque




class LidarLiteChild(Lidar_Lite):
  'LidarLiteChild documentation'

  def __init__(self):
    super( LidarLiteChild, self ).__init__()
    print "LidarLiteChild constructor"
    self._running = True
    self.simulatedData = False

  def init(self):

    connected = lidarLiteChild.connect(1)

    #print "Connected = ", connected

    if connected >= 0:  #TODO Is this value correct???
      print "Lidar connected"

      try:
        lidarLiteChild.writeAndWait( 0x04, 0x0A )
        lidarLiteChild.writeAndWait( 0x11, 0x0A ) # Distance measurements per request.  Using 10.
        lidarLiteChild.writeAndWait( 0x1C, 0x60 ) # Reduce sensitivity and errors per manual.
      except:
        print "Lidar not available."
        print "Using simulated data."
        self.simulatedData = True

      return True
#end if

    else:
      print "Lidar not connected."
      return False



  def terminate(self):
    self._running = False
  
  def run(self):
    xRange = []
    maxItemsInQueue = 10
    measurements = deque(xRange, maxItemsInQueue)

    while self._running:

      if self.simulatedData:
        distanceCM = 25.4
        distanceInch = distanceCM / 2.54
      else:
        distanceCM = self.getDistance()
        distanceInch = distanceCM / 2.54

#      print "Inches:  ", distanceInch

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

initOk = lidarLiteChild.init()

if initOk:

  #Create Thread
  lidarLiteChildThread = Thread(target=lidarLiteChild.run)

  #Start Thread
  lidarLiteChildThread.start()

  while True:
    command = raw_input("Command: ")
    cmd = command[0]
    if cmd == 'q' or cmd == 'Q':
      break

  lidarLiteChild.terminate()
  print "Thread finished"

else:
  print "Shutting down"

