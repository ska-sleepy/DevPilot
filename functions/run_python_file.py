import os
import subprocess

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

            output = f"STDOUT: {python_process.stdout}\nSTDERR: {python_process.stderr}"

            if python_process.returncode != 0:
                return f"Process exited with code {python_process.returncode}\n{output}"

            if python_process.stdout == "" and python_process.stderr == "":
                return "No output produced."

            return output
        except subprocess.TimeoutExpired:
            return "Error: process timed out after 30 seconds"
        except Exception as e:
            return f"Error executing Python file: {e}"
    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file and returns its output, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The filepath to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "description": "Arguments to pass to the Python file.",
                    "items": {"type": "string"},
                },
            },
            "required": ["file_path"],
        },
    },
}
