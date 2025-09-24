import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# --- CONFIGURACIÓN ---
load_dotenv()
app = Flask(__name__)

# --- CORS MEJORADO ---
# Configuración específica para WordPress
CORS(app, 
     origins=["https://vaitengewon.club", "https://www.vaitengewon.club"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Accept", "Origin", "X-Requested-With"],
     supports_credentials=True
)

# --- ENDPOINT PRINCIPAL ---
@app.route("/analizar-idea", methods=['POST', 'OPTIONS'])
def analizar_idea():
    # Manejar preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'https://vaitengewon.club')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept')
        return response
    
    datos_recibidos = request.get_json()
    if not datos_recibidos:
        return jsonify({"error": "No se recibieron datos"}), 400

    print("--- DATOS RECIBIDOS DESDE WORDPRESS ---")
    print(datos_recibidos)
    print("---------------------------------------")

    wp_user_id = datos_recibidos.get('wp_user_id')
    print(f"Análisis solicitado por el usuario con ID de WP: {wp_user_id}")

    respuesta_para_wordpress = {
        "status": "exito",
        "mensaje": "Datos recibidos correctamente por el cerebro de Python.",
        "usuario_id_confirmado": wp_user_id
    }
    
    response = jsonify(respuesta_para_wordpress)
    response.headers.add('Access-Control-Allow-Origin', 'https://vaitengewon.club')
    return response

# Ruta de verificación
@app.route("/")
def index():
    return "El Cerebro IA está online y listo para recibir datos en /analizar-idea."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)