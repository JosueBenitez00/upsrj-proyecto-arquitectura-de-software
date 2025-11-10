from datetime import datetime
from uuid import uuid4
from src.domain.models import BinaryFile

class UploadBinaryUseCase:
    def __init__(self, file_repo, db_repo):
        self.file_repo = file_repo
        self.db_repo = db_repo
        
    def execute(self, file, environment: str) -> BinaryFile:
        binary_id = str(uuid4())
        filename = self.file_repo.save_file(file, binary_id)
        binary = BinaryFile(
            id=binary_id,
            filename=filename,
            environment=environment,
            status='pending' if environment == 'prod' else 'signed',
            uploaded_date=datetime.now()
        )
        # Convert binary to dict for storage
        binary_dict = {
            'file_id': binary.id,
            'filename': binary.filename,
            'environment': binary.environment,
            'status': binary.status,
            'uploaded_date': binary.uploaded_date.isoformat()
        }
        self.db_repo.add_record(binary_dict)
        return binary