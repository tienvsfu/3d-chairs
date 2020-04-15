import trimesh
import os
import json
import re

#get output obj's file name
def output_obj_name(argument): 
    switcher = { 
        "chair_back": "back.obj", 
        "chair_arm": "arm.obj", 
        "chair_seat": "seat.obj", 
        "chair_base": "leg.obj"
    } 
    return switcher.get(argument, "unknown") 

#get input IDs from command line
# 173,347,470,515,688,1095,1325,2820,3001,39101
inputs = input("Please enter test IDs (e.g. 173,347,470,515,688,1095,1325,2820,3001,39101):\n")
selected_test_cases = re.findall('\d+', inputs)

#iterate all the test IDs
for test_case in selected_test_cases:
    #read json
    with open("data/in/" + test_case + "/result.json") as f:
        data = json.load(f)

    #create new folder for each test ID
    if not os.path.isdir('data/out/' + test_case + '/'):
        os.mkdir('data/out/' + test_case + '/')

    #to deal with symmetric sets of arms, symmetric sets of legs, etc.
    repeat_flag = 0
    last_output_obj_name = ''

    for first_children in data[0]['children']:
        #get obj file name
        get_output_obj_name = output_obj_name(first_children["name"])
        
        #set a flag to combine symmetric sets of same object 
        if (get_output_obj_name == last_output_obj_name ):
            repeat_flag = 1;
        else:
            repeat_flag = 0;

        #create a scene
        if (repeat_flag == 0):
            scene = trimesh.Scene()

        #append each object to each scene
        for second_children in first_children['children']:
            if 'children' in second_children:#if else in case here has no children 
                for third_children in second_children['children']:
                    for objs in third_children['objs']:
                        filepath = "data/in/" + test_case + "/objs/"+ objs + ".obj"
                        if os.path.isfile(filepath) and os.path.exists(filepath):#ignore missing files
                            scene.add_geometry(trimesh.load(filepath))
            else:
                for objs in second_children['objs']:
                        filepath = "data/in/" + test_case + "/objs/"+ objs + ".obj"
                        if os.path.isfile(filepath) and os.path.exists(filepath):#ignore missing files
                            scene.add_geometry(trimesh.load(filepath))

        #again to deal with symmetric sets.
        last_output_obj_name = get_output_obj_name
        
        #export obj file
        scene.export('data/out/' + test_case + '/' + get_output_obj_name)
        
