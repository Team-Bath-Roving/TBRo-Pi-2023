import cv2
import imagezmq
from imutils.video import VideoStream

class SteamManager:
	"""
	Handles sending camera images from rover to laptop
	"""
	def __init__(self, CAMS, LAPTOP_IP="localhost", JPEG_QUALITY=50):
		"""
		Parameters
		----------
		CAMS : list
			Two-dimensional list containing information about each camera
		LAPTOP_IP : str
			IP address of laptop
		JPEG_QUALITY : int
			Quality of image to be sent to laptop (0 to 100)
		"""
		if LAPTOP_IP == "localhost":
			self.sender = imagezmq.ImageSender()
		else:
			self.sender = imagezmq.ImageSender(connect_to=f"tcp://{LAPTOP_IP}:5555") # port has to be 5555
		
		self.streams = [
			[name, VideoStream(i, usePiCamera=PiCam).start()] for name, i, PiCam in CAMS
		]
		self.JPEG_QUALITY = JPEG_QUALITY

	def send_frames(self):
		"""
		Loops through each video streams and sends a frame to the laptop
		"""
		for name, stream in self.streams:

			# Read frame
			frame = stream.read()

			# Resize
			sf = 1
			# if name == "Webcam":
			# 	sf = 0.4
			# else:
			# 	sf = 0.8
			frame = cv2.resize(frame, (0,0,), fx=sf, fy=sf)

			# Compress
			frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.JPEG_QUALITY])[1]

			# Send frame
			self.sender.send_image(name, frame)