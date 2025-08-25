import os
from config import charatar_limit

def get_file_content(working_directory, file_path):
    try:
        file_path_dir = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.realpath(file_path_dir)
         
        if not absolute_file_path.startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        file = open(file_path_dir, "r")
        file_content = file.read()

        if len(file_content) <= charatar_limit:
            return file_content[0:10000] + f"\n[...File \"{file_path}\" truncated at 10000 characters]"
        return file_content
    
    except Exception as e:
        return f"Error: {e}"
