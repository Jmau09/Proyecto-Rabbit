"""Procesador: consume de 'recordatorios', aplica lógica (IA simulada)
y publica en 'procesados'. Se puede ejecutar de forma independiente.
"""
from conexion import conectar_rabbitmq
import time

def procesar_recordatorio(mensaje: str) -> str:
    msg = mensaje.strip()
    lower = msg.lower()
    # lógica simple, extensible con IA externa
    if 'pierna' in lower:
        return msg + ' 🦵🔥 ¡Día de pierna! Mantén buena forma.'
    if 'cardio' in lower:
        return msg + ' 🏃‍♂️💨 ¡Vamos con el cardio! 30 min.'
    if 'pesas' in lower or 'fuerza' in lower:
        return msg + ' 🏋️‍♂️ ¡Fuerza y técnica! Calienta antes.'
    return msg + ' 💪 ¡No te rindas hoy!'

def iniciar_procesador():
    conexion, canal = conectar_rabbitmq()
    print('[Procesador] Esperando mensajes en queue "recordatorios"...')
    def callback(ch, method, properties, body):
        texto = body.decode()
        print(f'[Procesador] Recibido: {texto}')
        procesado = procesar_recordatorio(texto)
        # simular tiempo de procesamiento/IA
        time.sleep(0.8)
        canal.basic_publish(exchange='', routing_key='procesados', body=procesado.encode())
        print(f'[Procesador] Publicado en "procesados": {procesado}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue='recordatorios', on_message_callback=callback)
    try:
        canal.start_consuming()
    except KeyboardInterrupt:
        print('Parando procesador...')
    finally:
        conexion.close()

if __name__ == '__main__':
    iniciar_procesador()
