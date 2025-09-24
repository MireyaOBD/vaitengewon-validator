import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Cargamos las variables de entorno (nuestra clave de OpenAI) desde el archivo .env
load_dotenv()

# Creamos la aplicación Flask
app = Flask(__name__)

# --- NUEVO ENDPOINT ---
# Esta es la dirección que nuestro WordPress llamará.
# El 'methods=['POST']' le dice a Flask que esta ruta solo acepta peticiones POST.
@app.route("/analizar-idea", methods=['POST'])
def analizar_idea():
    # 1. RECIBIR LOS DATOS
    # request.get_json() toma los datos JSON que nos envía el chat de WordPress.
    datos_recibidos = request.get_json()

    # Si no recibimos datos, devolvemos un error.
    if not datos_recibidos:
        return jsonify({"error": "No se recibieron datos"}), 400

    # 2. PROCESAR LOS DATOS (Por ahora, solo los mostraremos en la terminal)
    # Imprimimos los datos en nuestra terminal de Cursor para confirmar que han llegado.
    print("--- DATOS RECIBIDOS DESDE WORDPRESS ---")
    print(datos_recibidos)
    print("---------------------------------------")

    # Extraemos el ID del usuario para usarlo más adelante.
    wp_user_id = datos_recibidos.get('wp_user_id')
    print(f"Análisis solicitado por el usuario con ID de WP: {wp_user_id}")

    # 3. DEVOLVER UNA RESPUESTA DE CONFIRMACIÓN
    # Le respondemos a WordPress que hemos recibido los datos correctamente.
    # Esto es crucial para que el chat sepa que el envío fue exitoso.
    respuesta_para_wordpress = {
        "status": "exito",
        "mensaje": "Datos recibidos correctamente por el cerebro de Python.",
        "usuario_id_confirmado": wp_user_id
    }
    
    # jsonify() convierte nuestro diccionario de Python en un formato JSON válido.
    return jsonify(respuesta_para_wordpress)


# Esta es la ruta principal que ya teníamos, la dejamos para verificar que el server sigue online.
@app.route("/")
def index():
    return "El Cerebro IA está online y listo para recibir datos en /analizar-idea."

# Esto no cambia.
if __name__ == "__main__":
    app.run(debug=True)