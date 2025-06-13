import os, subprocess

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if file_path.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        err = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        print(err)
        return err
    if not os.path.exists(path):
        err = f'Error: File "{file_path}" not found.'
        print(err)
        return err
    if not os.path.isfile(path) or not file_path.endswith(".py"):
        err = f'Error: "{file_path}" is not a Python file.'
        print(err)
        return err

    try:
        result = subprocess.run(
            ["python3", path],
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
        output = "\n".join(out) if out else "No output produced."
        print(output)
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
