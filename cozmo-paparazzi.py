import cozmo
from cozmo.util import degrees
import time
import sys
import os

# GLOBALS
imageNumber = 0
directory = '.'


def on_new_camera_image(evt, **kwargs):
	pilImage = kwargs['image'].raw_image
	global directory
	pilImage.save(f"data/{directory}/{directory}-{kwargs['image'].image_number}.jpeg", "JPEG")

def cozmo_program(robot: cozmo.robot.Robot):
	
	# Make sure Cozmo's head and arm are at reasonable levels
	robot.set_head_angle(degrees(10.0)).wait_for_completed()
	robot.set_lift_height(0.0).wait_for_completed()

	# Set directory to the Category that Cozmo is going to photograph
	global directory
	directory = sys.argv[1]
	if not os.path.exists('data'):
		os.makedirs('data')
	if not os.path.exists(f'data/{directory}'):
		os.makedirs(f'data/{directory}')

	# Anytime Cozmo sees a "new" image, take a photo
	robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

	# Do this for 5 seconds, and then quit with a Lady Gaga quote
	time.sleep(5)
	print("I'm your biggest fan. I'll follow you until you love me")

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
