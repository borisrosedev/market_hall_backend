import os
from pathlib import Path

def allowed_file(filename, allowed_extensions):
    """ checks if a file extension is allowed """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions



def delete_file_in_uploads_folder(filename: str):
    """Delete a specific file in uploads folder safely"""
    uploads_folder = Path(os.getcwd()) / "uploads"
    #uploads_folder.mkdir(exist_ok=True)  # crée le dossier si besoin

    # build a normalized path
    file_path = (uploads_folder / filename).resolve()

    # check if file really is in uploads
    if uploads_folder.resolve() not in file_path.parents:
        print("Security error: attempted path traversal detected")
        return

    if file_path.exists():
        file_path.unlink()
        print(f"{filename} has been deleted successfully.")
    else:
        print(f"Error: {filename} does not exist in uploads folder.")

