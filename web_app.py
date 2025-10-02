from flask import Flask, render_template, request, jsonify
import threading
import time
from productor import enviar_recordatorio
from consumidor import iniciar_consumidor

app = Flask(__name__)

# In-memory store of processed messages (for UI). This is populated by the consumer callback.
mensajes_procesados = []

def agregar_mensaje(msg):
    # Guardar con timestamp breve
    mensajes_procesados.append({'texto': msg, 'ts': time.time()})
    # mantener sólo últimos 200
    if len(mensajes_procesados) > 200:
        mensajes_procesados.pop(0)

# Ejecutar consumidor en hilo de fondo para rellenar mensajes procesados
def start_bg_consumer():
    try:
        iniciar_consumidor(callback=agregar_mensaje)
    except Exception as e:
        print('Error al iniciar consumidor en background:', e)

t = threading.Thread(target=start_bg_consumer, daemon=True)
t.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cliente')
def cliente():
    return render_template('cliente.html')

@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.get_json() or {}
    usuario = data.get('usuario', '').strip()
    mensaje = data.get('mensaje', '').strip()
    if not usuario or not mensaje:
        return jsonify({'ok': False, 'error': 'usuario o mensaje vacío'}), 400
    full = f"{usuario} - {mensaje}"
    enviar_recordatorio(full)
    return jsonify({'ok': True, 'status': 'enviado a recordatorios'})

@app.route('/api/processed')
def api_processed():
    # devolver lista simple de textos, recientes primero
    return jsonify([m['texto'] for m in reversed(mensajes_procesados)])

@app.route('/api/users')
def api_users():
    # extraer usuarios desde mensajes procesados y enviados (simple)
    users = set()
    for m in mensajes_procesados:
        t = m['texto']
        if ' - ' in t:
            users.add(t.split(' - ', 1)[0])
    return jsonify(sorted(list(users)))

if __name__ == '__main__':
    # Evitar reloader para que el hilo no se duplique
    app.run(debug=False, use_reloader=False, port=5000)
