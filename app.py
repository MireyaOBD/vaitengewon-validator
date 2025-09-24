import os
import openai
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# --- CONFIGURACIÓN ---
load_dotenv()
app = Flask(__name__)

# Configura el cliente de OpenAI usando la clave de las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- FUNCIONES DE LÓGICA DE IA (EL PIPELINE) ---

def analizar_perfil_fundador(datos):
    """Paso 1: Analiza el perfil del usuario."""
    try:
        prompt = f"""
        Actúa como un coach de emprendimiento y analista de talento. Basado en la siguiente información:
        - Personalidad: {datos.get('personalidad_fundador')}
        - Pasiones: {datos.get('pasiones_fundador')}
        - Habilidades y Recursos: {datos.get('recursos_fundador')}
        - Estilo de Vida Deseado: {datos.get('estilo_vida_deseado')}

        Extrae 5 principios clave que definen el éxito y la satisfacción para esta persona.
        Luego, resume el perfil del emprendedor en un párrafo conciso.
        Devuelve tu respuesta en formato JSON con las claves "principios_clave" (una lista de strings) y "perfil_resumido" (un string).
        """
        response = openai.Completion.create(
            engine="text-davinci-003", # O el modelo que prefieras
            prompt=prompt,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )
        # Aquí procesaríamos la respuesta para convertirla en un diccionario Python
        # Por ahora, simularemos la salida
        print(">>> ANÁLISIS DE PERFIL REALIZADO (SIMULADO)")
        return {
            "principios_clave": ["Autonomía y flexibilidad", "Impacto creativo", "Estabilidad financiera", "Aprendizaje continuo", "Equilibrio vida-trabajo"],
            "perfil_resumido": "Un emprendedor creativo con una fuerte necesidad de autonomía. Valora la capacidad de generar un impacto tangible a través de sus habilidades, buscando un equilibrio que le permita disfrutar de un estilo de vida flexible sin sacrificar la estabilidad económica."
        }
    except Exception as e:
        print(f"Error en analizar_perfil_fundador: {e}")
        return None

# Aquí irían las otras funciones de la arquitectura (path de validación, path de generación, etc.)
# Por simplicidad, las simularemos por ahora.

def generar_html_resultado(perfil):
    """Paso Final: Genera el HTML a partir de los datos analizados."""
    
    principios_html = "".join([f"<li>{principio}</li>" for principio in perfil['principios_clave']])
    
    html = f"""
    <div style="font-family: sans-serif; line-height: 1.6;">
        <h3>Tu Perfil de Emprendedor</h3>
        <p>{perfil['perfil_resumido']}</p>
        <h4>Principios Clave para tu Éxito:</h4>
        <ul>{principios_html}</ul>
        <hr>
        <p><em>Este es un análisis preliminar. El análisis de mercado y de ideas se añadirá en los siguientes pasos.</em></p>
    </div>
    """
    print(">>> HTML DE RESULTADO GENERADO")
    return html

def enviar_resultado_a_wordpress(user_id, html_content):
    """Envía el resultado final de vuelta a WordPress."""
    url = os.getenv("WORDPRESS_API_URL")
    api_key = os.getenv("WORDPRESS_API_KEY")

    if not url or not api_key:
        print("Error: Faltan las variables de entorno WORDPRESS_API_URL o WORDPRESS_API_KEY")
        return False
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key
    }
    payload = {
        'wp_user_id': user_id,
        'html_result': html_content
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta es 4xx o 5xx
        print(f">>> Respuesta de WordPress: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar datos a WordPress: {e}")
        return False


# --- ENDPOINT PRINCIPAL ---
@app.route("/analizar-idea", methods=['POST'])
def analizar_idea():
    datos_recibidos = request.get_json()
    if not datos_recibidos:
        return jsonify({"error": "No se recibieron datos"}), 400

    print("--- DATOS RECIBIDOS DESDE WORDPRESS ---")
    print(datos_recibidos)
    
    wp_user_id = datos_recibidos.get('wp_user_id')
    if not wp_user_id:
        return jsonify({"error": "Falta wp_user_id"}), 400

    # --- EJECUCIÓN DEL PIPELINE ---
    # 1. Analizar perfil
    perfil_analizado = analizar_perfil_fundador(datos_recibidos)
    if not perfil_analizado:
        return jsonify({"error": "Fallo en el análisis del perfil"}), 500
    
    # (Aquí irían los pasos 2 y 3: bifurcación y path de validación/generación)
    
    # 4. Generar HTML
    html_final = generar_html_resultado(perfil_analizado)

    # 5. Enviar de vuelta a WordPress
    exito_envio = enviar_resultado_a_wordpress(wp_user_id, html_final)
    
    if not exito_envio:
        return jsonify({"error": "Fallo al guardar el resultado en WordPress"}), 500

    # 6. Devolver respuesta de éxito al chat
    return jsonify({
        "status": "exito",
        "mensaje": "Análisis completado y guardado en WordPress."
    })

@app.route("/")
def index():
    return "El Cerebro IA está online."