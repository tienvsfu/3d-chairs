
## Quickstart
`python main.py`
`python main.py --input-path ./data/bunch_of_chairs --output-path output/`

### Dependencies
* pyrender
* tensorflow
* trimesh 
* numpy
* a banana :)

patch pyrender:
Pyrender has a bug where it cannot render the depth image correctly, to apply a patch for this bug:
* The patch is originally at: https://github.com/mmatl/pyrender/pull/40
* Find the location where pyrender is installed: pip show pyrender | grep Location
* Note down the installed location from the above command, add "pyrender" to the end: .../site-packages/pyrender
* Overwrite the camera.py and renderer.py files included in the pyrender_patch directory of this project in the above directory

note: 
there seems to be a bug with trimesh
i did some research online and it seems different versions of trimesh behave differently
https://github.com/mikedh/trimesh/issues/504
while it doesn't break the code (just need to run a few times)
i just want to put a heads-up warning here.
