import RPi.GPIO as GPIO
import time
import smtplib

sender='viruskilled@gmail.com'
receivers='pratap.sps20@gmail.com,aishhwar.singh3@gmail.com'

message="""From: Raspberry pi
Breach Detected at home. Take Action.
"""
username='viruskilled@gmail.com'
password='***********'
server=smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
GPIO.setmode(GPIO.BCM)
 
# Define GPIO to use on Pi
GPIO_PIR = 7
 
print "PIR Module Test (CTRL-C to exit)"
 
# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)
 
Current_State  = 0
Previous_State = 0
 
try:
 
  print "Waiting for PIR to settle ..."
 
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0
 
  print "  Ready"
 
  # Loop until users quits with CTRL-C
  while True :
 
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
 
    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      print "  Motion detected!"
      GPIO.setup(24,GPIO.OUT)
      GPIO.output(24,0)
      GPIO.output(24,1)
      time.sleep(3)
      GPIO.output(24,0)
      
      server.login(username,password)
      server.sendmail(sender,receivers,message)
      
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      print "  Ready"
      Previous_State=0
 
    # Wait for 10 milliseconds
    time.sleep(0.01)
 
except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()