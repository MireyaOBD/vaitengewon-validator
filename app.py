import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import openai
import json

# --- CONFIGURACIÓN ---
load_dotenv()
app = Flask(__name__)

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

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

# --- FUNCIONES DE ANÁLISIS DE NEGOCIO ---
def analyze_business_ideas(user_data):
    """
    Analiza las respuestas del usuario y genera ideas de negocio con análisis de viabilidad
    """
    try:
        # Construir prompt para OpenAI
        prompt = f"""
Eres un consultor experto en emprendimiento y análisis de viabilidad de negocios. 

ANÁLISIS DEL EMPRENDEDOR:
- Punto de partida: {user_data.get('punto_de_partida', 'No especificado')}
- Personalidad: {user_data.get('personalidad_fundador', 'No especificado')}
- Pasiones: {user_data.get('pasiones_fundador', 'No especificado')}
- Recursos y habilidades: {user_data.get('recursos_fundador', 'No especificado')}
- Estilo de vida deseado: {user_data.get('estilo_vida_deseado', 'No especificado')}

TAREA:
Genera 5 ideas de negocio específicas y viables basadas en el perfil del emprendedor.

Para cada idea, proporciona:
1. Nombre de la idea
2. Descripción breve (2-3 líneas)
3. Análisis de viabilidad de mercado (demanda, competencia, tendencias)
4. Análisis de viabilidad personal (recursos, habilidades, personalidad, estilo de vida)
5. Calificación final de viabilidad (1-5, donde 5 es muy viable y 1 es viable pero necesita más recursos)

FORMATO DE RESPUESTA (JSON):
{{
    "ideas": [
        {{
            "nombre": "Nombre de la idea",
            "descripcion": "Descripción breve",
            "viabilidad_mercado": "Análisis de mercado",
            "viabilidad_personal": "Análisis personal",
            "calificacion": 4,
            "razon_calificacion": "Explicación de por qué esta calificación"
        }}
    ]
}}

Responde ÚNICAMENTE con el JSON válido, sin texto adicional.
"""

        # Llamar a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un consultor experto en emprendimiento. Responde siempre en formato JSON válido."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        # Procesar respuesta
        content = response.choices[0].message.content.strip()
        
        # Limpiar respuesta si tiene markdown
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        
        # Parsear JSON
        analysis_result = json.loads(content)
        
        logger.info(f"Análisis completado exitosamente. Ideas generadas: {len(analysis_result.get('ideas', []))}")
        return analysis_result
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parseando JSON de OpenAI: {e}")
        return {"error": "Error procesando respuesta de IA", "ideas": []}
    except Exception as e:
        logger.error(f"Error en análisis de OpenAI: {e}")
        return {"error": f"Error en análisis: {str(e)}", "ideas": []}

def generate_html_report(analysis_data, user_data):
    """
    Genera HTML estructurado para mostrar en WordPress
    """
    try:
        ideas = analysis_data.get('ideas', [])
        if not ideas:
            return "<p>No se pudieron generar ideas de negocio. Intenta nuevamente.</p>"
        
        html = f"""
        <div class="vaitengewon-analysis-report">
            <h2>🚀 Análisis de Ideas de Negocio</h2>
            <div class="analysis-summary">
                <p><strong>Emprendedor:</strong> {user_data.get('personalidad_fundador', 'No especificado')}</p>
                <p><strong>Área de interés:</strong> {user_data.get('punto_de_partida', 'No especificado')}</p>
                <p><strong>Objetivo de vida:</strong> {user_data.get('estilo_vida_deseado', 'No especificado')}</p>
            </div>
            
            <div class="business-ideas-container">
        """
        
        for i, idea in enumerate(ideas, 1):
            calificacion = idea.get('calificacion', 1)
            stars = "★" * calificacion + "☆" * (5 - calificacion)
            
            html += f"""
                <div class="business-idea-card">
                    <div class="idea-header">
                        <h3>💡 Idea #{i}: {idea.get('nombre', 'Sin nombre')}</h3>
                        <div class="viability-score">
                            <span class="stars">{stars}</span>
                            <span class="score">{calificacion}/5</span>
                        </div>
                    </div>
                    
                    <div class="idea-content">
                        <p class="idea-description">{idea.get('descripcion', 'Sin descripción')}</p>
                        
                        <div class="viability-analysis">
                            <h4>📊 Análisis de Viabilidad</h4>
                            <div class="market-analysis">
                                <h5>Mercado:</h5>
                                <p>{idea.get('viabilidad_mercado', 'Sin análisis')}</p>
                            </div>
                            <div class="personal-analysis">
                                <h5>Personal:</h5>
                                <p>{idea.get('viabilidad_personal', 'Sin análisis')}</p>
                            </div>
                            <div class="rating-explanation">
                                <h5>Justificación de la calificación:</h5>
                                <p>{idea.get('razon_calificacion', 'Sin justificación')}</p>
                            </div>
                        </div>
                    </div>
                </div>
            """
        
        html += """
            </div>
            
            <div class="analysis-footer">
                <p><em>Análisis generado por Vaitengewon IA - {timestamp}</em></p>
            </div>
        </div>
        
        <style>
        .vaitengewon-analysis-report {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        
        .analysis-summary {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .business-idea-card {
            border: 1px solid #ddd;
            border-radius: 12px;
            margin-bottom: 20px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .idea-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .idea-header h3 {
            margin: 0;
            font-size: 1.2em;
        }
        
        .viability-score {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stars {
            color: #ffd700;
            font-size: 1.2em;
        }
        
        .score {
            background: rgba(255,255,255,0.2);
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .idea-content {
            padding: 20px;
        }
        
        .idea-description {
            font-size: 1.1em;
            margin-bottom: 15px;
            color: #333;
        }
        
        .viability-analysis h4 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .viability-analysis h5 {
            color: #555;
            margin-bottom: 8px;
            font-size: 0.95em;
        }
        
        .market-analysis, .personal-analysis, .rating-explanation {
            margin-bottom: 12px;
        }
        
        .analysis-footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
        }
        </style>
        """
        
        return html
        
    except Exception as e:
        logger.error(f"Error generando HTML: {e}")
        return f"<p>Error generando reporte: {str(e)}</p>"

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

        # Procesar datos del usuario
        logger.info(f"[{timestamp}] Iniciando análisis de ideas de negocio...")
        
        # Analizar ideas de negocio con OpenAI
        analysis_result = analyze_business_ideas(datos_recibidos)
        
        if analysis_result.get('error'):
            logger.error(f"[{timestamp}] Error en análisis: {analysis_result['error']}")
            return jsonify({
                "status": "error",
                "mensaje": f"Error en el análisis: {analysis_result['error']}",
                "usuario_id_confirmado": wp_user_id,
                "timestamp": timestamp
            }), 500
        
        # Generar HTML para WordPress
        html_report = generate_html_report(analysis_result, datos_recibidos)
        
        respuesta_para_wordpress = {
            "status": "exito",
            "mensaje": "Análisis de ideas de negocio completado exitosamente.",
            "usuario_id_confirmado": wp_user_id,
            "timestamp": timestamp,
            "analisis_completo": analysis_result,
            "html_report": html_report,
            "ideas_generadas": len(analysis_result.get('ideas', []))
        }
        
        response = jsonify(respuesta_para_wordpress)
        response.headers.add('Access-Control-Allow-Origin', '*')
        logger.info(f"[{timestamp}] Análisis completado. Ideas generadas: {len(analysis_result.get('ideas', []))}")
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