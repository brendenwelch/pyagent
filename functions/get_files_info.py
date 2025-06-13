import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, directory)

    if directory.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    contents = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        contents.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
    return "\n".join(contents)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
