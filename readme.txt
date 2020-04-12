464 project:
1) pre-process: group segments (blender) --> done
2) parse: convert to internal representation (trimesh) --> done
3) mix: randomly generate model --> done
4) match: fix connections (make it pretty) --> wip
5) score: calculate score for new object --> wip


require: 
* anaconda (for trimesh)
* trimesh 
* numpy
* a banana

install anaconda: 
* download anaconda (python 3.7): https://www.anaconda.com/distribution/#linux
* terminal: bash ~/Downloads/Anaconda3-2020.02-Linux-x86_64.sh
* say yes to everything

install trimesh:
* terminal: conda install -c conda-forge trimesh
* terminal: pip install trimesh[easy]

install numpy:
* pip install numpy

