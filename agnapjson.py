from pathlib import Path
import json

'''passwords={"passwords":[
   {"date":None,"service":"google", "username":"ranga","password":"none"}   
]}'''



def write_json(data_as_dictionary,file_name_with_path):
    '''need to provide data to be written as in dictionary format and json file location with full path'''
    with open(file=file_name_with_path,mode='w') as file:
        json.dump(data_as_dictionary,file,indent=1)


def read_and_ament_json(file_name_with_path,name_of_the_exisiting_dictionary:str,new_dictionary_data_to_be_added):
    '''input json file name with path, 
        name of existing dictionary object (example "passwords"is the object of this file) 
        and new dictionary dta to be appended to existing dictionary'''
    with open(file=file_name_with_path,mode='r') as file:
        data=json.load(file)
        temp_data=data[name_of_the_exisiting_dictionary]
        temp_data.append(new_dictionary_data_to_be_added)
        #write new data to the file
        write_json(data,file_name_with_path)

def remove_and_ament_json(file_name_with_path,name_of_the_existing_dictionary:str,row_index:int):
    '''input json file name with path, 
        name of existing dictionary object (example "passwords"is the object of this file) 
        and index of the row where record need to be removed'''
    with open(file=file_name_with_path,mode='r') as file:
        data=json.load(file)
        temp_data=data[name_of_the_existing_dictionary]
        temp_data.pop(row_index)
        #write new data to the file
        write_json(data,file_name_with_path)


