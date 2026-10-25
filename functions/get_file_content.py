import os
from config import MAX_CHARS

def get_file_content(working_directory,file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir,file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot list "{file_path}"as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'...File "{file_path}" truncated at {MAX_CHARS} characters'
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the contents of a file within the permitted working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path to the file to read from the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}


google_schema_get_file_content = {
    "name": "get_file_content",
    "description": "Read the contents of a file within the permitted working directory.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "file_path": {
                "type": "STRING",
                "description": "Relative path to the file to read from the working directory.",
            },
        },
        "required": ["file_path"],
    },
}