from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)

def call_function(call, verbose=False):
    if verbose:
        print(f"Calling function: {call.name}({call.args})")
    else:
        print(f" - Calling function: {call.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python": run_python_file,
    }

    if call.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=call.name,
                    response={"error": f"Unknown function: {call.name}"},
                )
            ],
        )

    args = dict(call.args)
    args["working_directory"] = "./calculator"

    result = function_map[call.name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=call.name,
                response={"result": result},
            )
        ],
    )
