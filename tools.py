from pathlib import Path
import shutil
from datetime import datetime


def list_folder(path: str):
    """A function to list the files in a directory(folder)"""
    try: 

        folder = Path(path)
        
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder}")
        if not folder.is_dir():
            raise NotADirectoryError(f"Directory does not exist: {folder}")
        
        files = [f.name for f in folder.iterdir() if f.is_file()]
        return files
    
    except Exception as e:
        return f"Error: {e}"
    
def make_folder(path: str):
    """Function to make a folder. If the folder does not exist it creates the parents and the folder.
    If it does then it does nothing"""
    try:
        folder = Path(path)
        folder.mkdir(parents=True, exist_ok=True)
        return f"Folder created (or already exists): {folder.resolve()}"
    except Exception as e:
        return f"Error: {e}"


def rename_move_file(source_path: str, destination: str):
    """A function to move a file from one folder or path to another.
    If the parent path does not exist for the destination, it creates it"""

    try:
        src = Path(source_path)
        dest = Path(destination)

        if not src.exists():
            raise FileNotFoundError(f"Source file {src} does not exist")
        if not src.is_file():
            raise ValueError(f"Source path is not a file: {src}")
        
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest = dest / src.name if dest.is_dir() else dest

        shutil.move(src, dest)
        return f"{src.name} has been moved to {dest}"

    except Exception as e:
        return f"Error: {e}"


def delete_file_or_folder(path: str):
    """A function to delete a file or a folder"""

    try:
        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(f"Can't delete {file} since it doesn't exist")
        if file.is_dir():
            shutil.rmtree(file)
            return f"Directory {file} has been deleted successfully"
        elif file.is_file():
            file.unlink(missing_ok=True)
            return f"{file} has been deleted successfully"
        else:
            return f"{file} is neither a file nor a folder"

    except Exception as e:
        return f"Error: {e}"


def get_file_info(path: str):
    """A function that returns the stats of a file given the path"""
    try:
        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(f"The file {file.name} does not exist")
        if not file.is_file():
            raise ValueError(f"The path {path} is not a file.")
        
        stats = file.stat()
        
        result = {
            "name": file.name,
            "file_size": f"{round(stats.st_size / 1024)} MB",
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "created": datetime.fromtimestamp(stats.st_birthtime).strftime("%Y-%m-%d %H:%M:%S")
        }

        return result

    except Exception as e:
        return f"Error: {e}"


def copy_file_or_folder(source_path: str, destination: str):
    """A function to copy a file or folder from source to destination"""
    try:
        src = Path(source_path)
        dest = Path(destination)

        if not src.exists():
            raise FileNotFoundError(f"The file or folder {src} does not exist")
        if src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)
            return f"The folder {src} has been copied to {dest} successfully"
        elif src.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            return f"The file {src.name} has been copied to {dest} successfully"
        else:
            return f"{src} is neither a file nor a folder"

    except Exception as e:
        return f"Error: {e}"

def empty_folder(path: str):
    try:
        folder = Path(path)

        if not folder.exists():
            raise FileNotFoundError(f"The folder {folder} does not exist.")
        if not folder.is_dir():
            raise ValueError(f"The path {folder} is not a folder")
        
        for file in folder.iterdir():
            delete_file_or_folder(file)

        return f"Folder {folder} has been emptied successfully"

    except Exception as e:
        return f"Error: {e}"
    
def get_folder_info(path: str):
    try:
        folder = Path(path)

        if not folder.exists():
            raise FileNotFoundError(f"The folder {folder} does not exist.")
        if not folder.is_dir():
            raise NotADirectoryError(f"The path {folder} is not a directory.")
        
        stats = folder.stat()
        
        file_sizes = [round(file.stat().st_size / 1024) for file in folder.iterdir() if file.is_file()]
        total_size = sum(file_sizes)
        number_of_files = len(file_sizes) 

        result = {
            "name": folder.name,
            "folder_size": f"{total_size} MB",
            "number_of_files": f"{number_of_files} file" if number_of_files == 1 else f"{number_of_files} files",
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "created": datetime.fromtimestamp(stats.st_birthtime).strftime("%Y-%m-%d %H:%M:%S")
        }

        return f"Here is the folder info: {result}"
    except Exception as e:
        return f"Error: {e}"
    
get_folder_info(r"C:\Users\MSI\Projects")