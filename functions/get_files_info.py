import os

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)
    path = os.path.join(working_directory, directory)

    if directory.startswith("/") or not os.path.abspath(path).startswith(working_directory):
        err = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        print(err)
        return err
    if not os.path.isdir(path):
        err = f'Error: "{directory}" is not a directory'
        print(err)
        return err

    contents = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        contents.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
    out = "\n".join(contents)
    print(out)
    return out
