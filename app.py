# app.py v5.0

import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI

# --- CONFIGURACIÓN ---
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/analizar-idea": {"origins": "https://vaitengewon.club"}})

# Cliente de OpenAI (sintaxis v1.0+)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- FUNCIONES DEL PIPELINE DE ANÁLISIS ---

def analyze_business_ideas(user_data):
    """
    Función principal que llama a OpenAI para analizar el perfil y generar 5 ideas de negocio.
    """
    print(">>> Iniciando análisis completo con OpenAI...")
    try:
        prompt = f"""
        Actúa como un consultor de negocios y estratega de startups de élite. Tu cliente es un emprendedor con el siguiente perfil:
        - Punto de Partida (Idea o Intención): {user_data.get('punto_de_partida', 'No especificado')}
        - Personalidad (Myers-Briggs): {user_data.get('personalidad_fundador', 'No especificado')}
        - Pasiones y Hobbies: {user_data.get('pasiones_fundador', 'No especificado')}
        - Recursos y Habilidades Actuales: {user_data.get('recursos_fundador', 'No especificado')}
        - Estilo de Vida Deseado: {user_data.get('estilo_vida_deseado', 'No especificado')}

        TU TAREA PRINCIPAL:
        Genera 5 ideas de negocio específicas, innovadoras y viables que se alineen perfectamente con el perfil completo del emprendedor. Si el emprendedor ya proporcionó una idea, úsala como inspiración para la primera idea y luego genera 4 alternativas superiores o complementarias. Y debes analizarlas respecto al mercado, para saber si es una idea que se emprenderá en un oceano azul o rojo.
        
        PARA CADA UNA DE LAS 5 IDEAS, DEBES PROPORCIONAR:
        1.  "nombre": Un nombre atractivo para la idea de negocio.
        2.  "descripcion": Una descripción concisa y potente (2-3 frases).
        3.  "viabilidad_mercado": Un análisis orientativo del mercado. Indica si es un océano azul o rojo, el potencial de ingresos (bajo, medio, alto) y si es compatible con el estilo de vida deseado.
        4.  "viabilidad_personal": Un análisis de la sinergia con el emprendedor. Evalúa cómo la idea se alinea con su personalidad, pasiones y habilidades. Identifica una habilidad clave (blanda o técnica, no financiera) que necesitaría desarrollar.
        5.  "calificacion": Una calificación numérica de 1 a 5 (donde 5 es máxima viabilidad).
        6.  "razon_calificacion": Una justificación breve y clara de por qué le diste esa calificación.

        FORMATO DE RESPUESTA OBLIGATORIO:
        Responde EXCLUSIVAMENTE con un objeto JSON válido que contenga una única clave "ideas", cuyo valor sea un array de los 5 objetos de idea. No incluyas ningún texto, explicación o markdown antes o después del JSON.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", # Modelo optimizado para JSON
            messages=[
                {"role": "system", "content": "Eres un consultor de negocios que solo responde con formato JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, # Un poco más creativo
            response_format={ "type": "json_object" }
        )

        resultado_texto = response.choices[0].message.content
        print(f">>> Respuesta JSON de OpenAI: {resultado_texto}")
        return json.loads(resultado_texto) # Devuelve el objeto Python directamente

    except Exception as e:
        print(f"!!! Error en la llamada a OpenAI (analyze_business_ideas): {e}")
        return {"error": f"Error en análisis de IA: {str(e)}", "ideas": []}

def generate_html_report(analysis_data):
    """
    Genera un informe HTML a partir de los datos analizados por la IA.
    """
    print(">>> Iniciando generación de reporte HTML...")
    try:
        ideas = analysis_data.get('ideas', [])
        if not ideas:
            return "<h3>Error en el Análisis</h3><p>La IA no pudo generar ideas de negocio en este momento. Por favor, intenta de nuevo con respuestas más detalladas.</p>"
        
        html_cards = ""
        for i, idea in enumerate(ideas, 1):
            calificacion = idea.get('calificacion', 1)
            stars = "★" * calificacion + "☆" * (5 - calificacion)
            
            html_cards += f"""
            <div class="idea-card">
                <div class="idea-header">
                    <h3>{i}. {idea.get('nombre', 'Sin Nombre')}</h3>
                    <div class="score">
                        <span class="stars">{stars}</span> ({calificacion}/5)
                    </div>
                </div>
                <div class="idea-body">
                    <p><strong>Descripción:</strong> {idea.get('descripcion', 'N/A')}</p>
                    <h4>Análisis de Viabilidad</h4>
                    <p><strong>Mercado (Océano/Potencial):</strong> {idea.get('viabilidad_mercado', 'N/A')}</p>
                    <p><strong>Sinergia Personal (Perfil/Habilidades):</strong> {idea.get('viabilidad_personal', 'N/A')}</p>
                    <p><strong>Justificación de la Calificación:</strong> <em>{idea.get('razon_calificacion', 'N/A')}</em></p>
                </div>
            </div>
            """
        
        # Estilos CSS embebidos para que se vea bien en WordPress sin depender de archivos externos
        styles = """
        <style>
            .vaitengewon-map-section .idea-card { border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            .vaitengewon-map-section .idea-header { background-color: #f7f5fa; padding: 15px; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: space-between; align-items: center; }
            .vaitengewon-map-section .idea-header h3 { margin: 0; font-family: 'Ubuntu', sans-serif; color: #7030A0; font-size: 1.2em; }
            .vaitengewon-map-section .score { font-weight: bold; color: #333; }
            .vaitengewon-map-section .score .stars { color: #ffc107; font-size: 1.3em; }
            .vaitengewon-map-section .idea-body { padding: 20px; }
            .vaitengewon-map-section .idea-body h4 { margin-top: 0; font-family: 'Ubuntu', sans-serif; color: #555; }
            .vaitengewon-map-section .idea-body p { margin-bottom: 10px; }
        </style>
        """
        
        print(">>> HTML generado exitosamente.")
        return styles + html_cards
        
    except Exception as e:
        print(f"!!! Error al generar el HTML: {e}")
        return "<p>Hubo un error al formatear el resultado del análisis.</p>"

def enviar_resultado_a_wordpress(user_id, html_content):
    """Envía el informe HTML de vuelta a WordPress."""
    print(">>> Iniciando envío a WordPress...")
    url = os.getenv("WORDPRESS_API_URL")
    api_key = os.getenv("WORDPRESS_API_KEY")

    if not url or not api_key:
        print("!!! Error: Faltan variables de entorno WORDPRESS_API_URL o WORDPRESS_API_KEY")
        return False
    
    headers = { 'Content-Type': 'application/json', 'X-API-KEY': api_key }
    payload = { 'wp_user_id': user_id, 'html_result': html_content }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f">>> Respuesta de WordPress: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"!!! Error al enviar datos a WordPress: {e}")
        return False

# --- ENDPOINT PRINCIPAL ---
@app.route("/analizar-idea", methods=['POST'])
def analizar_idea():
    datos_recibidos = request.get_json()
    if not datos_recibidos: return jsonify({"error": "No se recibieron datos"}), 400
    
    print("\n--- INICIO DE NUEVA SOLICITUD ---")
    
    analysis_result = analyze_business_ideas(datos_recibidos)
    if "error" in analysis_result:
        return jsonify({"error": analysis_result["error"]}), 500
    
    html_final = generate_html_report(analysis_result)
    
    exito_envio = enviar_resultado_a_wordpress(datos_recibidos.get('wp_user_id'), html_final)
    if not exito_envio:
        return jsonify({"error": "Fallo al guardar el resultado en WordPress"}), 500

    return jsonify({"status": "exito", "mensaje": "Análisis completado y guardado en WordPress."})

# Ruta de verificación
@app.route("/")
def index():
    return "El Cerebro IA está online."