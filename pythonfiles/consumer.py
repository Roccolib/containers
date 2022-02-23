from kafka import KafkaConsumer
import requests
import flask
from flask import Flask,jsonify,json

 #8 test pour commit 12h09 le 1703

consumer=KafkaConsumer(
    'topicDiscMessage',
    bootstrap_servers = ['localhost:29092'],
    group_id='test-consumer-group',
#    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=True
)
#lancer le module Flask à l'execution de l'api
app = flask.Flask(__name__)
#pas d'affichage des details des messages d erreur
app.config["DEBUG"] = False
#decrire l'acces a partir de root/messahesKafka limité a la fonction POST depuis le WEB
@app.route('/Consumer',  methods=['POST'])


def consume_messages():
    consumer.commit()
    while True:
        message_batch = consumer.poll()
        for msg in consumer:
            CCO2 = msg.value
#            print(msg)
#            print(CCO2)
            headers = {"HTTP_HOST": "MyVeryOwnHost", "User-Agent": "topicDiscMessage" }
            urlConsum = 'http://localhost:5000/orchestrator'
#            urlConsum = 'http://co22tok.westeurope.cloudapp.azure.com:5000/orchestrator'
            payCO2 = requests.post(url = urlConsum, data = CCO2, headers = headers)

if __name__ == '__main__':
    consume_messages()
app.run(debug=False, port=5002, host='0.0.0.0')
