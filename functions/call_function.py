import json
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from config import working_directory

def call_function(tool_call, verbose=False):
    function_name = tool_call.function.name
    if verbose:
        print(f"Calling function: {function_name}({tool_call.function.arguments})")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return f"Unknown function: {function_name}"

    args = json.loads(tool_call.function.arguments)
    args["working_directory"] = working_directory
    return function_map[function_name](**args)
