import os
from google.genai import types

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if file_path.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(path, "r") as file:
        contents = file.read()
    if len(contents) > 10000:
        contents = contents[:10000] + f"...File {file_path} truncated at 10000 characters"
    return contents

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read contents from, relative to the working directory.",
            ),
        },
    ),
)
