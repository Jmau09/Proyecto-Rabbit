import pika

def conectar_rabbitmq(host='localhost'):
    """Conecta con RabbitMQ y declara las colas necesarias."""
    params = pika.ConnectionParameters(host)
    conexion = pika.BlockingConnection(params)
    canal = conexion.channel()
    # cola de entrada y cola de salida
    canal.queue_declare(queue='recordatorios', durable=True)
    canal.queue_declare(queue='procesados', durable=True)
    return conexion, canal
