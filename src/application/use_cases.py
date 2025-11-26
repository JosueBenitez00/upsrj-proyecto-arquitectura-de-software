from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any , Optional
from src.domain.models import BinaryFile

from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.file_repository import FileRepository

class UploadBinaryUseCase:
    def __init__(self, file_repo, db_repo):
        self.file_repo = file_repo
        self.db_repo = db_repo
        
    def execute(self, file, enviroment: str) -> BinaryFile:
        binary_id = str(uuid4())
        filename = self.file_repo.save_file(file, binary_id)
        binary = BinaryFile(
            id=binary_id,
            filename=filename,
            environment=enviroment,
            status='pending' if enviroment == 'prod' else 'signed',
            uploaded_date=datetime.now()
        )
        self.db_repo.add(binary)
        return binary

class ListFilesUseCase:
    
    def __init__(self, db_repo: JsonRepository):
        self.db_repo = db_repo
        
    def execute(self) -> List[Dict[str, Any]]:
        try:
            records = self.db_repo.list_records()
            return records
        except Exception as e:
            print(f"[ListFilesUseCase] Error retrieving records: {e}")
            return []


class SignBinaryUseCase:
    def __init__(self, file_repo: FileRepository, db_repo: JsonRepository):
        self.file_repo = file_repo
        self.db_repo = db_repo

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        try:
            binary = self.db_repo.get_by_id(file_id)
            if binary:
                return BinaryFile(file_id=file_id, status='signed')
            return None
        except Exception as e:
            print(f"[SignBinaryUseCase] Error signing binary: {e}")
            return None