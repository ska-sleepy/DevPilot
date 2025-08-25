import os

def write_file(working_directory, file_path, content):
    try:
        file_path_dir = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.realpath(file_path_dir)
         
        if not absolute_file_path.startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        try:
            with open(file_path_dir, 'w') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
        
    except Exception as e:
        return f"Error: {e}"
    

