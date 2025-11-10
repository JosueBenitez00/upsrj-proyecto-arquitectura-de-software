import os
import shutil
from werkzeug.utils import secure_filename

class FileRepository:
    def __init__(self, upload_dir: str = "src/data/binaries"):
        self.upload_dir = upload_dir
        self.__ensure_upload_directory()
    
    def __ensure_upload_directory(self) -> None:
        """Ensure the upload directory exists."""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
    
    def save_file(self, file, binary_id: str) -> str:
        """Save an uploaded file and return the filename."""
        if file is None or file.filename == '':
            raise ValueError("No file provided")
        
        filename = secure_filename(f"{binary_id}_{file.filename}")
        filepath = os.path.join(self.upload_dir, filename)
        file.save(filepath)
        
        return filename
    
    def get_file(self, filename: str) -> str:
        """Get the full path of a stored file."""
        return os.path.join(self.upload_dir, filename)
    
    def delete_file(self, filename: str) -> bool:
        """Delete a stored file."""
        filepath = os.path.join(self.upload_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
