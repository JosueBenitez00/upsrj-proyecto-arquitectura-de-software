from dataclasses import dataclass
from datetime import datetime

@dataclass
class BinaryFile:
    id: str
    filename: str
    environment: str  # dev o prod
    status: str  # pending, approved, signed, rejected
    uploaded_date: datetime
    signed_path: str = None
    signature: str = None
    
    