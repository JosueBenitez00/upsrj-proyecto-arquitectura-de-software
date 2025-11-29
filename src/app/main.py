import sys
import os
from pathlib import Path

# Ajuste de rutas
sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from flask_mail import Mail
from src.app.routes import register_routes
from src.common.vars import HOME_HOST

def create_app():
    app = Flask(__name__, template_folder='templates')

    # --- CONFIGURACIÓN DEL CORREO (GMAIL) ---
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    
 
    
    app.config['MAIL_USERNAME'] = 'beniteztrejojosue809@gmail.COM'  
    app.config['MAIL_PASSWORD'] = 'gmwr lzcn hvnx zqhe' 
    


    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    # Inicializar Flask-Mail
    app.mail = Mail(app)

    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    # Ejecutar con waitress en producción: establecer PRODUCTION=1 en el entorno
    prod = os.environ.get("PRODUCTION", "0").lower() in ("1", "true", "yes")
    if prod:
        try:
            from waitress import serve
        except Exception:
            print("Waitress no está instalado. Instálalo con: python -m pip install waitress")
            raise
        serve(app, host="0.0.0.0", port=int(HOME_HOST))
    else:
        app.run(host="0.0.0.0", port=int(HOME_HOST), debug=True)