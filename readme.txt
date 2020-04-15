464 project:
1) parse: convert segments to parts --> done
2) mix: select parts randomly to form a chair --> done
3) match: apply deformation and fix connection --> done
4) score: calculate score for new chair --> wip (thu dinh)

run:
* put the segmented chair in "data/in"
* enter python3 p.py to convert it to parts in "data/out"
* enter python3 mm.py to create a randomly generated chair "10.obj"
* enter python3 mm-layout.py to generate 6 chairs and display them

require: 
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

note: 
there seems to be a bug with trimesh
i did some research online and it seems different versions of trimesh behave differently
https://github.com/mikedh/trimesh/issues/504
while it doesn't break the code (just need to run a few times)
i just want to put a heads-up warning here.
