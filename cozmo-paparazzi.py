import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import sys
import os

# GLOBALS
imageNumber = 0
directory = '.'
liveCamera = False

def on_new_camera_image(evt, **kwargs):
	global liveCamera
	if liveCamera:
		pilImage = kwargs['image'].raw_image
		global directory
		pilImage.save(f"data/{directory}/{directory}-{kwargs['image'].image_number}.jpeg", "JPEG")

def move_to_next_side(robot: cozmo.robot.Robot):
	robot.turn_in_place(degrees(-45)).wait_for_completed()
	robot.drive_straight(distance_mm(400), speed_mmps(200), False, False, 0).wait_for_completed()
	robot.turn_in_place(degrees(130)).wait_for_completed()
	take_photos(robot)

def take_photos(robot: cozmo.robot.Robot):
	global liveCamera
	# Start photo sesh
	liveCamera = True
	time.sleep(1)
	robot.drive_straight(distance_mm(100), speed_mmps(100), False, False, 0).wait_for_completed()
	robot.drive_straight(distance_mm(-100), speed_mmps(100), False, False, 0).wait_for_completed()
	# Stop photo sesh
	liveCamera = False
	time.sleep(1)

def cozmo_program(robot: cozmo.robot.Robot):
	
	# Make sure Cozmo's head and arm are at reasonable levels
	robot.set_head_angle(degrees(10.0)).wait_for_completed()
	robot.set_lift_height(0.0).wait_for_completed()

	robot.say_text(f"I'm going to take photos of {sys.argv[1]}").wait_for_completed()

	# Set directory to the Category that Cozmo is going to photograph
	global directory
	directory = sys.argv[1]
	if not os.path.exists('data'):
		os.makedirs('data')
	if not os.path.exists(f'data/{directory}'):
		os.makedirs(f'data/{directory}')

	# Anytime Cozmo sees a "new" image, take a photo
	robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

	# Initial photo sesh
	robot.drive_straight(distance_mm(-200), speed_mmps(100), False, False, 0).wait_for_completed()
	take_photos(robot)

	# Get all the angles
	for i in range(3):
		move_to_next_side(robot)

	# And we're done here
	robot.say_text("All done!").wait_for_completed()
	robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()
	

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
