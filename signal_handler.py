#!/usr/bin/env python3
 
import signal
import time
 
# define the singal handler to modify standard behaviour when the process catches the SIGINT signal (CTRL-C)
# you can kill the process either from another terminal by finding its pid number or by CTRL-z to put in background
# and then kill -9 pid from the same terminal window
def sigint_handler(signum, frame):
    print("Stop pressing CTRL+C!")

#Install the signal handler
signal.signal(signal.SIGINT, sigint_handler)
 
# just an infinite loop that prints . and then sleeps for 1sec
while True:
    print(".")
    time.sleep(1)
 
