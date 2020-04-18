## Quickstart
`python main.py` or 
`python main.py --input-path ./data/bunch_of_chairs`

## Input Data
* Paste all the input data set folders in data/in before running the first command above
* Alternatively include the path to the input data set as in the second command above

## Output Data
* Output obj files and scores.txt are in data/in_generated

## Scorer
* Scorer checkpoint is available at https://drive.google.com/open?id=1aPOpeJ8n7dYpCFUMY14zChi_OWMFC1XO
* Please download and unzip it in scorer directory before running main.py to get the correct scores.
* If you want to use scorer to evaluate the test set you can call evaluate method in evaluate.py (refer to main.py)
* If you want to retrain the scorer with different data, use train.py and replace the data and model output directory

## Dependencies
* Refer to requirements.txt for full list of dependencies. The main packages are listed below:
** trimesh==3.6.20
** pyrender==0.1.39
** tensorflow==2.1.0
** numpy==1.18.1
** tqdm==4.42.1


## Patch
Pyrender has a bug where it cannot render the depth image correctly which would affect scorer, to apply a patch for this bug:
* The patch is originally at: https://github.com/mmatl/pyrender/pull/40
* Find the location where pyrender is installed: pip show pyrender | grep Location
* Note down the installed location from the above command, add "pyrender" to the end: .../site-packages/pyrender
* Overwrite the camera.py and renderer.py files included in the pyrender_patch directory of this project in the above directory
