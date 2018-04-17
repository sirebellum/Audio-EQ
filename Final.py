import threading
import time
import pyaudio
import wave

from myfunctions import clip16
import argparse

from streaming import wavstream
import socket
import paho.mqtt.client as mqtt

##########Parse CLI Arguments#############
parser = argparse.ArgumentParser()
parser.add_argument("RECEIVE_IP", help="Specify IP address to receive at")
parser.add_argument("PUBLISH_IP", help="Specify IP address to publish MQTT at")
args = parser.parse_args()

#########Class Function Initialisation#############
class Threading_func():
  def __init__(self):

        self.kill_process = False

        self.num_channels = 2         # Number of channels
        self.RATE = 44100        # Sampling rate (frames/second)

        #Initiate udp stream
        self.udpstream = wavstream(9001, args.RECEIVE_IP) #IP of local machine interface where receiving
        self.udpthread = threading.Thread(target=self.udpstream.start)
        self.udpthread.daemon = True #Kill thread when parent is dead
        self.udpthread.start()

################################################################
  def Pythread(self):
        # Open audio stream
        p = pyaudio.PyAudio()
        stream_enable = True
        try:
            stream = p.open(format      = pyaudio.paInt16,
                    channels    = self.num_channels,
                    rate        = self.RATE,
                    input       = False,
                    output      = True )

        except OSError:
            print("COULDN'T ACCESS AUDIO DEVICE")
            stream_enable = False
            pass

        index=0
        while not self.kill_process:

            while len(self.udpstream.data) <= index: #Wait for buffer to be filled

                #If process killed before stream received:
                if self.kill_process:
                    self.udpstream.data.append(0)
                    index = 0
                    break

            stream_string = self.udpstream.data[index]
            index=index+1
            if stream_enable: stream.write(stream_string)

        self.udpstream.kill_process = True
        if stream_enable:
            stream.stop_stream()
            stream.close()
        p.terminate()
        print ("**** Audio killed ****")

########## Main ############
a = Threading_func()
thread = threading.Thread(target=a.Pythread) #Thread for object "a" of class Thread
thread.daemon = True
thread.start()

time.sleep(1)
print("")

mqttc = mqtt.Client("python_pub")
if args.PUBLISH_IP != "0":
  mqttc.connect(args.PUBLISH_IP, 1883) # IP of RPi running LEDs
  #Turn on LED
  mqttc.publish("test/led", "ENGAGE")

try:
    input("Press enter to quit...")
    if args.PUBLISH_IP != "0":
      mqttc.publish("test/led", "DISENGAGE")
      mqttc.disconnect()
    a.kill_process = True
    time.sleep(1)
    exit("Done!")

except KeyboardInterrupt:
    if args.PUBLISH_IP != "0":
      mqttc.publish("test/led", "DISENGAGE")
      mqttc.disconnect()
    a.kill_process = True
    time.sleep(1)
    exit("interrupted")
