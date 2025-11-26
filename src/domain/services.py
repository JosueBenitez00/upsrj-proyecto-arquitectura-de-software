import hashlib
from typing import Optional, Tuple

# Asegúrate de importar tus repositorios y modelos aquí
# from repositories import FileRepository, JsonRepository
# from models import BinaryFile 

class SigningService:
    def sign_file(self, binary: 'BinaryFile') -> Tuple[str, bytes]:
        try:
            source_path = binary.filename

            # Compute SHA-256 signature
            sha256_hash = hashlib.sha256()
            with open(source_path, 'rb') as file:
                content = file.read()
                sha256_hash.update(content)

            signature = sha256_hash.hexdigest()
            signed_content = content + b"\n\n# SIGNATURE: " + signature.encode("utf-8")

            print(f"[SigningService] File '{binary.filename}' signed successfully.")
            return signature, signed_content

        except Exception as e:
            print(f"[SigningService] Error while signing '{binary.filename}': {e}")
            raise

class SignBinaryUseCase:
    def __init__(self, file_repo: 'FileRepository', json_repo: 'JsonRepository', signing_service: SigningService):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service
            
    def execute(self, file_id: str) -> Optional['BinaryFile']:
        record = self.json_repo.get_record(file_id)

        if record is None:
            print(f"[SignBinaryUseCase] Record not found for file id: {file_id}")
            return None

        try:
            # Asegurar que sea instancia de BinaryFile
            # Nota: Asegúrate de que BinaryFile esté importado y definido
            binary = record if isinstance(record, BinaryFile) else BinaryFile.from_dict(record)

            # Firmar el archivo (devuelve firma y contenido firmado)
            signature, signed_content = self.signing_service.sign_file(binary)

            # Guardar archivo firmado usando el repositorio
            signed_path = self.file_repo.save(signed_content, file_id=binary.id, signed=True)

            # Actualizar entidad
            binary.status = "signed"
            binary.signature = signature
            binary.signed_path = signed_path

            # Persistir cambios en el registro JSON
            self.json_repo.update_record(
                binary.id,
                {
                    "status": binary.status,
                    "signed_path": binary.signed_path,
                    "signature": binary.signature
                }
            )

            print(f"[SignBinaryUseCase] File '{binary.filename}' signed and saved successfully.")
            return binary

        except Exception as e:
            print(f"[SignBinaryUseCase] Error while signing file '{file_id}': {e}")
            return None