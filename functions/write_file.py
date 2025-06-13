import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if file_path.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        err = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        print(err)
        return err

    if not os.path.exists(path):
        os.makedirs("/".join(path.split("/")[:-1]), exist_ok=True)
    with open(path, "w") as file:
        file.write(content)
    out = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    print(out)
    return out
