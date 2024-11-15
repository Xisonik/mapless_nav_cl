
cameras = ['fr_link6/visuals/cam02_root/cam02_parent/Camera_2', 
           'fl_link6/visuals/cam03_root/cam03_parent/Camera_3', 
           'box2_Link/visuals/cam01_root/cam01_parent/Camera_1']

usd_local_path = '/home/kit/.local/share/ov/pkg/isaac-sim-4.1.0/standalone_examples/Aloha/assets/aloha/aloloha_v03_cameras.usd'

robot_path = "/World/aloha"

image_saved_path = "/home/kit/.local/share/ov/pkg/isaac-sim-4.1.0/standalone_examples/Aloha/"

from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.manipulators import SingleManipulator
from omni.isaac.manipulators.grippers import ParallelGripper
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.franka.controllers import PickPlaceController
from omni.isaac.core.objects import DynamicCuboid
import carb
import sys
import numpy as np
from omni.isaac.sensor import Camera
import omni.replicator.core as rep
import os
from PIL import Image

my_world = World(stage_units_in_meters=1.0)
my_world.scene.add_default_ground_plane()

asset_path = usd_local_path

add_reference_to_stage(usd_path=asset_path, prim_path=robot_path)

my_world.reset()

depth_annotators = dict()
cameras_dict = dict()

def set_up_camera() -> None:
    """Setup camera sensors based on config paths

    Args:
        ...
    """
    for camera_relative_path in cameras:
        camera_path = os.path.join(robot_path, camera_relative_path)
        camera_name = camera_relative_path.split('/')[-1]

        print(camera_relative_path)
        print(camera_path)

        camera = Camera(
            prim_path=camera_path,
            name = camera_name
            )

        camera.initialize()
        camera.add_motion_vectors_to_frame()

        depth_annotators[camera_name] = rep.AnnotatorRegistry.get_annotator("distance_to_camera")
        depth_annotators[camera_name].attach([camera._render_product_path])

        cameras_dict[camera_name] = camera

    return

def save_image(i:int) -> None:
    for camera_relative_path in cameras:
        camera_path = os.path.join(robot_path, camera_relative_path)
        camera_name = camera_relative_path.split('/')[-1]

        depth = depth_annotators[camera_name].get_data()
        rgb = cameras_dict[camera_name].get_rgba()[:, :, :3] 

        try:                
            image = Image.fromarray(rgb)
            rgb_saved_path =  os.path.join(image_saved_path, camera_name + f'_{i}_rgb')
            image.save(rgb_saved_path, format="PNG")

            depth_image = Image.fromarray(depth).convert("L")
            depth_path =  os.path.join(image_saved_path, camera_name + f'_{i}_depth')
            depth_image.save(depth_path, format="PNG")
        except:
            pass

set_up_camera()

i = 0
while simulation_app.is_running():
    my_world.step(render=True)
    if my_world.is_playing():
        if my_world.current_time_step_index == 0:
            my_world.reset()

        observations = my_world.get_observations()

        save_image(i)

        i = i + 1


simulation_app.close()