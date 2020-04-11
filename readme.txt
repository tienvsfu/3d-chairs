464 project:

steps:
1) pre-process: use blender to group parts into: seat, leg, back, arm --> done
2) parse: convert to internal representation (trimesh) --> done
3) mix: randomly load and assemble parts --> done
4) match: fix connections to make it pretty --> wip
4) score: generate images for the scorer --> wip

require: 
* anaconda (for trimesh)
* trimesh 
* numpy

install anaconda: 
* download anaconda (python 3.7): https://www.anaconda.com/distribution/#linux
* terminal: bash ~/Downloads/Anaconda3-2020.02-Linux-x86_64.sh
* say yes to everything

install trimesh:
* terminal: conda install -c conda-forge trimesh
* terminal: pip install trimesh[easy]

install numpy:
* pip install numpy

