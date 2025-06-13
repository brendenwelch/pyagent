import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if file_path.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(path):
        os.makedirs("/".join(path.split("/")[:-1]), exist_ok=True)
    with open(path, "w") as file:
        file.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the specified file, creating it and all parent directories if they don't exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write contents to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the file."
            )
        },
    ),
)
