import os

def get_input_file():
    print("Drop your .txt path here (or drag and drop the file):")
    raw_path = input().strip().strip("\"'")
    if raw_path.startswith(('(', '[')) and raw_path.endswith((')', ']')):
        raw_path = raw_path[1:-1]
    return os.path.abspath(os.path.expanduser(raw_path))