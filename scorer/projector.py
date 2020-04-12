import os
import numpy as np
import pyrender
import trimesh
import matplotlib.pyplot as plt
from numpy import linalg as LA
from pyrender.constants import RenderFlags as RF

RX_TOP_MATRIX = np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]])
RY_LEFT_MATRIX = np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
RY_RIGHT_MATRIX = np.array([[0,0,-1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]])

class ObjProjector:
    def __init__(self, obj_dir):
        self.OBJ_DIR = obj_dir
    
    # def _normalize(self, depth):
    #     max_depth = np.max(depth)
    #     min_depth = np.min(depth)
    #     norm_depth = (depth-min_depth)/(max_depth-min_depth)

    def _get_projection(self, tm_mesh, dimension):
        tm_scene = tm_mesh.scene()
        
        tm_scene = tm_scene.scaled(0.8/np.max(tm_scene.extents))
        scene = pyrender.Scene.from_trimesh_scene(tm_scene)

        camera = pyrender.OrthographicCamera(xmag=0.5, ymag=0.5)
        camera_position = tm_mesh.scene().camera_transform
        scene.add(camera, pose=camera_position)

        #light = pyrender.DirectionalLight(intensity=1.0)
        #light_position = camera_position
        #scene.add(light, pose=light_position)

        r = pyrender.OffscreenRenderer(dimension, dimension)
        depth_buffer = r.render(scene, flags=RF.DEPTH_ONLY)
        r.delete()

        return depth_buffer

    def project(self, dimension, file_name):
        file_dir = os.path.join(self.OBJ_DIR, file_name)
        print(file_dir)

        # Front projection
        tm = trimesh.load(file_dir)
        depth_front = self._get_projection(tm, dimension)

        #Get top angle image
        tm_top = tm.copy().apply_transform(RX_TOP_MATRIX)
        depth_top = self._get_projection(tm_top, dimension)

        #Get left angle image
        tm_left = tm.copy().apply_transform(RY_LEFT_MATRIX)
        depth_left = self._get_projection(tm_left, dimension)
        
        #Get right angle image
        tm_right = tm.copy().apply_transform(RY_RIGHT_MATRIX)
        depth_right = self._get_projection(tm_right, dimension)
        
        # obj = np.multiply(LA.norm(np.mean(color, axis=2)), depth)
        return depth_front, depth_top, depth_left, depth_right#, obj


'''
Projector class is used to project obj object to different angle (front, top, left, right)
To test, uncomment the code below, put in correct path to model and run
'''
projector = ObjProjector('../../Chair/models')
front, top, left, right = projector.project(800, '172.obj')

fig, axs = plt.subplots(2, 2, figsize=(13, 13))
axs[0, 0].imshow(front, cmap=plt.cm.gray_r)
axs[0, 0].set_title('Front')
axs[0, 1].imshow(top, cmap=plt.cm.gray_r)
axs[0, 1].set_title('Top')
axs[1, 0].imshow(left, cmap=plt.cm.gray_r)
axs[1, 0].set_title('Left')
axs[1, 1].imshow(right, cmap=plt.cm.gray_r)
axs[1, 1].set_title('Right')
plt.tight_layout()
plt.show()
   