import os

def list_files(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."

def list_directories(directory):
    try:
        return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."
