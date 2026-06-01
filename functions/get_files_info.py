import os

def get_files_info(working_directory, directory="."):
    try:
        dir = os.path.join(working_directory, directory)
        absolute_dir = os.path.realpath(dir)

        if not absolute_dir.startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.exists(dir):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(dir):
            return f'Error: "{directory}" is not a directory'
        
        
        dir_contents = os.listdir(dir)
        ret = []
        for file in dir_contents:
            try:
                file_path = os.path.join(dir, file)
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                ret.append(f"- {file}: file_size={file_size}, is_dir={is_dir}")
            except Exception as e:
                return f"Error: {e}"
        return "\n".join(ret)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                },
            },
        },
    },
}
    
