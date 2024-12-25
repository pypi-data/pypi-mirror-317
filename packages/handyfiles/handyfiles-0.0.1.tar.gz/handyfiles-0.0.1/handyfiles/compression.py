import shutil

def compress_directory(directory, archive_name):
    try:
        shutil.make_archive(archive_name, 'zip', directory)
        return f"Directory '{directory}' compressed to '{archive_name}.zip'."
    except Exception as e:
        return f"Error: {e}"

def extract_archive(archive_path, extract_to):
    try:
        shutil.unpack_archive(archive_path, extract_to)
        return f"Archive '{archive_path}' extracted to '{extract_to}'."
    except FileNotFoundError:
        return f"Error: Archive '{archive_path}' not found."
    except Exception as e:
        return f"Error: {e}"
