import os
import subprocess

def run_python_file(working_directory, file_path, args = None ):
    
    
    try:
        # Get absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        # Run the file
        cmd = ['python', abs_file_path]
        if args:
            cmd.extend(args)
        
        result = subprocess.run(cmd, cwd=abs_working_dir, capture_output=True, text=True)
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file in the working directory, optionally passing command-line arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path to the Python file to run.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python file.",
                },
            },
            "required": ["file_path"],
        },
    },
}


google_schema_run_python_file = {
    "name": "run_python_file",
    "description": "Execute a Python file in the working directory, optionally passing command-line arguments.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "file_path": {
                "type": "STRING",
                "description": "Relative path to the Python file to run.",
            },
            "args": {
                "type": "ARRAY",
                "items": {"type": "STRING"},
                "description": "Optional command-line arguments to pass to the Python file.",
            },
        },
        "required": ["file_path"],
    },
}
