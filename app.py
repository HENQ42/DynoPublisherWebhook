import pika
import json
import time
import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS  # Import the CORS extension

# Cria uma instância do Flask
app = Flask(__name__)
CORS(app)

# Configurações do RabbitMQ
EXCHANGE_NAME = 'wppconnect'
QUEUE_NAME = 'chatbot-vicent'
ROUTING_KEY = ''

# Acessa a variável de ambiente CLODUAMQP_URL e faz o parse (fallback para localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

def setup_rabbitmq(channel):
    # Declara a exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)
    # Declara a fila
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    # Vincula a fila à exchange
    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)

# Conecta ao RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url))
channel = connection.channel()

# Configura a exchange, fila e binding
setup_rabbitmq(channel)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    body = request.get_json()

    if body.get('event') in ("onmessage", "onlogout"):
        # Envia a mensagem
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY, body=json.dumps(body).encode('utf-8'))
        print(f"Mensagem enviada: {body}")
    
    return 'OK', 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
