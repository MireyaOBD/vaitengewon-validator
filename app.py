import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS # <-- 1. Importamos la nueva herramienta

# --- CONFIGURACIÓN ---
load_dotenv()
app = Flask(__name__)

# --- 2. HABILITAMOS CORS ---
# Esto le dice a nuestro servidor: "Permito peticiones desde cualquier origen".
# Para producción, podríamos restringirlo solo a 'vaitengewon.club'. Por ahora, esto es suficiente.
CORS(app) 

# --- ENDPOINT PRINCIPAL (sin cambios) ---
@app.route("/analizar-idea", methods=['POST'])
def analizar_idea():
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
    
    return jsonify(respuesta_para_wordpress)

# Ruta de verificación (sin cambios)
@app.route("/")
def index():
    return "El Cerebro IA está online y listo para recibir datos en /analizar-idea."