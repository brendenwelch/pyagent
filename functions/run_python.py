import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if file_path.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.isfile(path) or not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python3", path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            timeout=30,
            text=True,
            capture_output=True,
            cwd=working_directory
        )
        out = []
        if result.stdout:
            out.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            out.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            out.append(f"Process exited with code {result.returncode}")
        return "\n".join(out) if out else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, relative to the working directory.",
            )
        },
    ),
)
