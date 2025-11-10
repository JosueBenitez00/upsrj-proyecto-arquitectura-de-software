from flask import request, jsonify, render_template
from src.application.use_cases import UploadBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository

def register_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_binary():
        try:
            file = request.files.get('file')
            environment = request.form.get('environment', 'dev')
            
            if not file:
                return jsonify({'error': 'No file provided'}), 400
            
            use_case = UploadBinaryUseCase(FileRepository(), JsonRepository())
            binary = use_case.execute(file, environment)
            
            return jsonify({
                'id': binary.id,
                'filename': binary.filename,
                'status': binary.status,
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
             
