import trimesh
import os
import json
import re
import tqdm
import pdb

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

# inputs = input("Please enter test IDs (e.g. 173,347,470,515,688,1095,1325,2820,3001,39101):\n")

def parse(in_path, out_path, chair_ids):
    chair_dirs = [d for d in os.listdir(in_path) if d.isdigit()]

    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    if chair_ids != 'all':
        chair_dirs = [d for d in chair_dirs if d in chair_ids.split(',')]

    print("Converting chair files...")
    for chair_dir in tqdm.tqdm(chair_dirs):
        chair_path = os.path.join(in_path, chair_dir, 'result.json')
        chair_path_out = os.path.join(out_path, chair_dir)

        with open(chair_path) as f:
            data = json.load(f)

        #create new folder for each test ID
        if not os.path.isdir(chair_path_out):
            os.mkdir(chair_path_out)

        #to deal with symmetric sets of arms, symmetric sets of legs, etc.
        repeat_flag = 0
        last_output_obj_name = ''

        for first_children in data[0]['children']:
            #print('test1')
            #get obj file name
            get_output_obj_name = output_obj_name(first_children["name"])
            
            #set a flag to combine symmetric sets of same object 
            if (get_output_obj_name == last_output_obj_name ):
                repeat_flag = 1
            else:
                repeat_flag = 0

            #create a scene
            if (repeat_flag == 0):
                scene = trimesh.Scene()

            #append each object to each scene
            for second_children in first_children['children']:
                #print('test2') 
                if 'children' in second_children:#if else in case here has no children
                    for third_children in second_children['children']:
                        #print('test3') 
                        if 'children' in third_children: 
                            for fourth_children in third_children['children']:
                                #print('test4')
                                if 'children' in fourth_children: 
                                    for fifth_children in fourth_children['children']:
                                        #print('test5')
                                        for obj in fifth_children['objs']:
                                            filepath = os.path.join(in_path, chair_dir, 'objs', f'{obj}.obj')
                                            # filepath = "data/in/" + test_case + "/objs/"+ objs + ".obj"
                                            if os.path.isfile(filepath) and os.path.exists(filepath):#ignore missing files
                                                scene.add_geometry(trimesh.load(filepath))
                                else:
                                    for obj in fourth_children['objs']:
                                        # filepath = "data/in/" + test_case + "/objs/"+ objs + ".obj"
                                        filepath = os.path.join(in_path, chair_dir, 'objs', f'{obj}.obj')                                        
                                        if os.path.isfile(filepath) and os.path.exists(filepath):#ignore missing files
                                            scene.add_geometry(trimesh.load(filepath))
                        else:
                            for obj in third_children['objs']:
                                # filepath = "data/in/" + test_case + "/objs/"+ objs + ".obj"
                                filepath = os.path.join(in_path, chair_dir, 'objs', f'{obj}.obj')
                                if os.path.isfile(filepath) and os.path.exists(filepath):#ignore missing files
                                    scene.add_geometry(trimesh.load(filepath))
                else:
                    for obj in second_children['objs']:
                        # filepath = "data/in/" + test_case + "/objs/"+ objs + ".obj"
                        filepath = os.path.join(in_path, chair_dir, 'objs', f'{obj}.obj')
                        if os.path.isfile(filepath) and os.path.exists(filepath):#ignore missing files
                            scene.add_geometry(trimesh.load(filepath))

            #again to deal with symmetric sets.
            last_output_obj_name = get_output_obj_name
            
            #export obj file
            scene.export(os.path.join(chair_path_out, get_output_obj_name))
