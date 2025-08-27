import os
from google.genai import types
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
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file in the specified filepath, if there isn't a file there file gets created located in the filepath , filepath constrained by the working_directory ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to get the file from relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description= "the content that is written to the file"
            )
        },
    ),
)
