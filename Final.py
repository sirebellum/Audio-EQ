import threading
import time
import pyaudio
import wave

from myfunctions import clip16

from streaming import wavstream
import socket   
  
#########Class Function Initialisation#############  
class Threading_func():
  def __init__(self):
  
        self.kill_process = False

        self.num_channels = 2         # Number of channels
        self.RATE = 44100        # Sampling rate (frames/second)
        
        #Initiate udp stream
        self.udpstream = wavstream(9001, "127.0.0.1") #IP of local machine interface where receiving
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

#Turn on LED
MESSAGE = "ENGAGE"
UDP_IP = '127.0.0.1' #IP of RPi running LEDs
UDP_PORT = 9002
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

#Prepare to turn off LED
MESSAGE = "DISENGAGE"

try:
    input("Press enter to quit...")
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    a.kill_process = True
    time.sleep(1)
    exit("Done!")
    
except KeyboardInterrupt:
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    a.kill_process = True
    time.sleep(1)
    exit("interrupted")
