# CONFIG
# Network information
LAPTOP_IP = "localhost"

# Camera information (name, index, PiCam?)
CAMS = [
	["Cam 1", 0, False]
]

# Level of compression
JPEG_QUALITY = 50 # (0=worst, 100=best quality)

# ========================================================

# Import libraries
import cv2
import time
import queue
import random

# Import classes
from classes.StreamManager import SteamManager
from classes.RoverSockets import SocketTimeout, FeedbackSend, CommandReceive

# Main function
def main_function(command_queue):
	# Create and connect feedback socket, then send confirmation message
	sock = FeedbackSend(LAPTOP_IP, 5002)
	sock.connect()

	# Set up StreamManager to handle video streams
	sm = SteamManager(CAMS, LAPTOP_IP, JPEG_QUALITY)
	time.sleep(1.0) # Need to give time for cameras to get ready
	
	# Log initial time and frequency to send feedback/ images
	FREQUENCY = 1 / 30
	prev_time = time.perf_counter()

	# Initialise empty feedback dict
	fb = {}

	done = False
	while not done:
		
		# Unload commands from queue
		while not command_queue.empty():
			commands = command_queue.get()
			# [Temp] print all commands
			print(commands)
			
			for command in commands:

				# Quitting
				if command == "QUIT_ROVER":
					print("Quit instruction received, exiting")
					sock.stop()
					raise SystemExit

				# *** handle other commands
				# ***

		# Send feedback and images
		if time.perf_counter() - prev_time > FREQUENCY:

			# Send frames to laptop
			sm.send_frames()

			# Send feedback
			sock.send(fb)
			fb = {}
			prev_time = time.perf_counter()


if __name__ == "__main__":
	command_queue = queue.Queue(0)
	command_sock = CommandReceive(command_queue, 5001)
	command_sock.start()

	main_function(command_queue)