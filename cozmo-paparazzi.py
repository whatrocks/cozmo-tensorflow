import cozmo
from cozmo.util import degrees

def cozmo_program(robot: cozmo.robot.Robot):
	robot.set_head_angle(degrees(10.0)).wait_for_completed()
	robot.set_lift_height(0.0).wait_for_completed()
	print("I'm your biggest fan. I'll follow you until you love me")

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
