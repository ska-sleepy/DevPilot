import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        file_path_dir = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.realpath(file_path_dir)
         
        if not absolute_file_path.startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        
        if not os.path.exists(file_path_dir):
            return f'Error: File "{file_path}" not found.'
        
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        try:
            python_process = subprocess.run(["uv", "run", file_path_dir, *args], timeout=30, 
                                            capture_output=True, text=True,)
            
            completed_process = [python_process.stdout, python_process.stderr] 

            if python_process.returncode != 0:
                raise Exception(f"Process exited with code {python_process.returncode}")
            
            elif completed_process[0] == "" and completed_process[1] == "":
                return "No output produced."
            
            else:
                return f"STDOUT: {completed_process[0]} \n STDERR: {completed_process[1]}"
        except Exception as e:
            return f"Error: executing Python file: {e}"
    except Exception as e:
        f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the given python file that is specified by the file_path and return the output produced by the file, filepath constrained by the working_directory ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to get the file from relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments that are used to run the python file",
                items=types.Schema(type=types.Type.STRING)
                )
            },
        ),
    )

                      
            
