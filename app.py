from flask import Flask, request, jsonify, send_from_directory
import base64
import time
import os
import re

app = Flask(__name__)

# carpeta donde se guardan firmas
UPLOAD_FOLDER = "firmas"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    response = send_from_directory('.', 'index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.json.get('imagen')
    nombre_doc = request.json.get('nombre', f"firma_{int(time.time())}")

    if not data or not isinstance(data, str):
        return jsonify({"error": "No hay imagen válida"}), 400

    try:
        if ',' in data:
            img_b64 = data.split(',')[1]
        else:
            img_b64 = data
            
        if len(img_b64) > 5 * 1024 * 1024:
            return jsonify({"error": "Imagen demasiado grande"}), 400

        # Limpiar el nombre para que sea un archivo válido
        safe_name = re.sub(r'[^a-zA-Z0-9_\-\s]', '_', nombre_doc).strip()
        filename = f"{safe_name}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(img_b64))

        return jsonify({"ok": True, "file": filename})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error interno al procesar la imagen"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)