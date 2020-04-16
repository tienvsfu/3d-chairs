464 project:
1) parse: convert segments to parts
2) mix: generate chair
3) match: apply deformation and fix connections
4) score: calculate score

run:
* place inputs in "data/in"
* modify c1 and c2 in "m.py" to match input ids  
* enter in terminal: python3 m.py 

require: 
* pyrender
* tensorflow
* anaconda (for trimesh)
* trimesh 
* numpy
* a banana :)

install anaconda: 
* download anaconda (python 3.7): https://www.anaconda.com/distribution/#linux
* terminal: bash ~/Downloads/Anaconda3-2020.02-Linux-x86_64.sh
* say yes to everything

install trimesh:
* terminal: conda install -c conda-forge trimesh
* terminal: pip install trimesh[easy]

install numpy:
* pip install numpy

install pyrender:
* pip install pyrender

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
