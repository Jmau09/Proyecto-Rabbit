"""Consumidor: consume de 'procesados' y muestra/entra al callback.
Puede ejecutarse standalone o ser usado por web_app para rellenar historial."""
from conexion import conectar_rabbitmq

def iniciar_consumidor(callback=None):
    conexion, canal = conectar_rabbitmq()
    print('[Consumidor] Escuchando cola "procesados"...')
    def callback_interno(ch, method, properties, body):
        texto = body.decode()
        print(f'[Consumidor] Recibido: {texto}')
        if callback:
            callback(texto)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue='procesados', on_message_callback=callback_interno)
    try:
        canal.start_consuming()
    except KeyboardInterrupt:
        print('Parando consumidor...')
    finally:
        conexion.close()

if __name__ == '__main__':
    iniciar_consumidor()
