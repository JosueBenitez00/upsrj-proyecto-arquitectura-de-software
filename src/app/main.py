import os
import sys
from flask import Flask

# Add parent directory to path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.app.routes import register_routes
from src.vars import HOME_HOST

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templaces'))
    app = Flask(__name__, template_folder=template_dir)
    register_routes(app)
    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HOME_HOST, debug=True)
    
    
    
    
    
