from conexion import conectar_rabbitmq

def enviar_recordatorio(mensaje: str):
    conexion, canal = conectar_rabbitmq()
    canal.basic_publish(exchange='',
                        routing_key='recordatorios',
                        body=mensaje.encode(),
                        properties=None)
    print(f"[Productor] Recordatorio enviado: {mensaje}")
    conexion.close()

if __name__ == '__main__':
    # envío de prueba
    enviar_recordatorio('UsuarioTest - Recuerda tu entrenamiento de pierna a las 18:00')
