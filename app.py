import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# --- CONFIGURACIÓN ---
load_dotenv()
app = Flask(__name__)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] Solicitud recibida en /analizar-idea - Método: {request.method}")
    logger.info(f"[{timestamp}] Headers: {dict(request.headers)}")
    logger.info(f"[{timestamp}] IP remota: {request.remote_addr}")
    
    # Manejar preflight OPTIONS request
    if request.method == 'OPTIONS':
        logger.info(f"[{timestamp}] Procesando preflight OPTIONS request")
        response = jsonify({'status': 'ok', 'message': 'CORS preflight successful'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Origin, X-Requested-With')
        response.headers.add('Access-Control-Max-Age', '86400')
        return response
    
    try:
        datos_recibidos = request.get_json()
        if not datos_recibidos:
            logger.warning(f"[{timestamp}] No se recibieron datos JSON")
            logger.info(f"[{timestamp}] Raw data: {request.get_data()}")
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        logger.info(f"[{timestamp}] --- DATOS RECIBIDOS DESDE WORDPRESS ---")
        logger.info(f"[{timestamp}] Datos: {datos_recibidos}")
        logger.info(f"[{timestamp}] ---------------------------------------")

        wp_user_id = datos_recibidos.get('wp_user_id')
        logger.info(f"[{timestamp}] Análisis solicitado por el usuario con ID de WP: {wp_user_id}")

        respuesta_para_wordpress = {
            "status": "exito",
            "mensaje": "Datos recibidos correctamente por el cerebro de Python.",
            "usuario_id_confirmado": wp_user_id,
            "timestamp": timestamp,
            "datos_recibidos": datos_recibidos
        }
        
        response = jsonify(respuesta_para_wordpress)
        response.headers.add('Access-Control-Allow-Origin', '*')
        logger.info(f"[{timestamp}] Respuesta enviada exitosamente")
        return response
        
    except Exception as e:
        logger.error(f"[{timestamp}] Error procesando solicitud: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

# --- ENDPOINTS DE DIAGNÓSTICO ---
@app.route("/")
def index():
    return "El Cerebro IA está online y listo para recibir datos en /analizar-idea."

@app.route("/health", methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": "vaitengewon-validator",
        "version": "1.0.0"
    })

@app.route("/test-cors", methods=['GET', 'POST', 'OPTIONS'])
def test_cors():
    """Endpoint para probar CORS desde WordPress"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] Test CORS endpoint called - Method: {request.method}")
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok', 'message': 'CORS test successful'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Origin, X-Requested-With')
        return response
    
    response = jsonify({
        "status": "success",
        "message": "CORS test successful",
        "timestamp": timestamp,
        "method": request.method,
        "headers_received": dict(request.headers)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/test-post", methods=['POST', 'OPTIONS'])
def test_post():
    """Endpoint para probar envío de datos POST"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] Test POST endpoint called")
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Origin, X-Requested-With')
        return response
    
    try:
        data = request.get_json() or {}
        logger.info(f"[{timestamp}] Test POST data received: {data}")
        
        response = jsonify({
            "status": "success",
            "message": "Test POST successful",
            "timestamp": timestamp,
            "data_received": data,
            "data_type": type(data).__name__
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        logger.error(f"[{timestamp}] Error in test POST: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)