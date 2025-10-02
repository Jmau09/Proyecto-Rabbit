# Fitness Notifier - Publisher/Subscriber con RabbitMQ

Estructura:
- productor -> publica en cola `recordatorios`
- procesador -> consume `recordatorios`, procesa (IA simulada) y publica en `procesados`
- consumidor -> consume `procesados` (puede ser standalone o embebido en web_app)

Instrucciones rápidas:
1. Asegúrate de tener RabbitMQ corriendo: `rabbitmq-server` o usando Docker:
   `docker run -d --hostname rabbit --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Opciones de ejecución:
   - Ejecutar procesador (proceso separado que transforma mensajes):
     ```bash
     python procesador.py
     ```
   - Ejecutar consumidor (si quieres ver por consola):
     ```bash
     python consumidor.py
     ```
   - Ejecutar la aplicación web (abrirá Admin y Cliente):
     ```bash
     python web_app.py
     ```

Flujo recomendado en dev:
- Ejecuta RabbitMQ.
- Ejecuta `python procesador.py` en una terminal.
- Ejecuta `python web_app.py` en otra terminal.
- Abre Admin (`/`) y Cliente (`/cliente`) en dos pestañas.
- Envía recordatorios desde Admin; el procesador los transformará y el consumidor en web los mostrará al cliente.
