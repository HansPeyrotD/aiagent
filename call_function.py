import json
from collections.abc import Callable

from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_files_info import schema_get_files_info, google_schema_get_files_info
from functions.get_file_content import schema_get_file_content, google_schema_get_file_content
from functions.run_python_file import schema_run_python_file, google_schema_run_python_file
from functions.write_file import schema_write_file, google_schema_write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

# Google GenAI-compatible wrapper for the current runtime.
google_available_functions = types.Tool(
    function_declarations=[
        google_schema_get_files_info,
        google_schema_get_file_content,
        google_schema_run_python_file,
        google_schema_write_file,
    ],
)


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = getattr(tool_call, "name", None)
    if function_name is None:
        function_name = getattr(getattr(tool_call, "function", None), "name", None)

    if function_name is None:
        raise ValueError("Tool call is missing a function name")

    raw_arguments = getattr(tool_call, "args", None)
    if raw_arguments is None:
        raw_arguments = getattr(getattr(tool_call, "function", None), "arguments", None) or "{}"

    if isinstance(raw_arguments, str):
        try:
            function_args = json.loads(raw_arguments)
        except json.JSONDecodeError:
            function_args = {}
    else:
        function_args = raw_arguments or {}

    if not isinstance(function_args, dict):
        function_args = {}

    tool_call_id = getattr(tool_call, "id", "")
    if not tool_call_id:
        tool_call_id = getattr(getattr(tool_call, "function", None), "id", "")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": f"Error: Unknown function: {function_name}",
        }

    function_args["working_directory"] = "./calculator"
    result = function_map[function_name](**function_args)

    result_message = {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": result,
    }

    if not result_message["content"]:
        raise ValueError(f"Function {function_name} returned empty content")

    return result_message
