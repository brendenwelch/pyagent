import os

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if file_path.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        err = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        print(err)
        return err
    if not os.path.isfile(path):
        err = f'Error: File not found or is not a regular file: "{file_path}"'
        print(err)
        return err

    with open(path, "r") as file:
        contents = file.read()
    if len(contents) > 10000:
        contents = contents[:10000] + f"...File {file_path} truncated at 10000 characters"
    print(f"Length: {len(contents)}")
    print(contents)
    return contents
