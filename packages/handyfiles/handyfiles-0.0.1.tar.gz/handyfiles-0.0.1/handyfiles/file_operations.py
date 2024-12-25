def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."

def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
            return f"Content written to '{file_path}'."
    except Exception as e:
        return f"Error: {e}"

def append_to_file(file_path, content):
    try:
        with open(file_path, 'a') as file:
            file.write(content)
            return f"Content appended to '{file_path}'."
    except Exception as e:
        return f"Error: {e}"
