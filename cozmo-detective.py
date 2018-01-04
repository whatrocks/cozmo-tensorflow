import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_lift_height(40.0).wait_for_completed()

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)