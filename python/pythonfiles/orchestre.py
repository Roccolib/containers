import flask
from flask import Flask,jsonify,json
from flask import request
import json
import requests
import hashlib


#lancer le module Flask à l'execution de l'api
app = flask.Flask(__name__)

#affichage des details des messages d erreur
app.config["DEBUG"] = True

#decrire l'acces a partir de root/messahesKafka limité a la fonction POST depuis le WEB
@app.route('/orchestrator', methods=['POST'])


def post_orchestrator():

#recuperation des metadonnées et payload reçus de la requête appelante
 payload = request.data
 contentType = request.headers.get('Content-Type')
 source = request.headers.get('User-Agent')
 topicNameDiscMessage = "topicDiscMessage"
 topicNamePending = "topicATraiter"
 topicNameCo2Extracted = "topicCO2Extracted"

# allowed format for incoming payload
 importables = ['application/json', 'text/plain', 'image/jpeg']
 try:
#envoi le contenu du forum vers producer
  if "Discourse" in source and contentType in importables:
   topicName = topicNameDiscMessage
   headers = {"HTTP_HOST": "MyVeryOwnHost", "topicName": topicName, "contentType": contentType }
   url = 'http://localhost:5001/messageBroker'
  # url = 'http://co22tok.westeurope.cloudapp.azure.com:5001/messageBroker'
   postObject = requests.post(url = url, data = payload, headers = headers)
   print(data)
   return("Message from forum sent to producer to kafka topic : topicDiscMessage")

#topic venant de consumer
  elif topicNameDiscMessage in source:
   payload = request.data
  #header à passer pour co2 extrated qui n' attend pas de topic name !
   headers = {"HTTP_HOST": "postMessageToExtractValue" }
   urlCO2Ext = 'http://localhost:5003/CO2extracted'
#   urlCO2Ext = 'http://co22tok.westeurope.cloudapp.azure.com:5003/CO2extracted'
   CO2ExtObject = requests.post(url = urlCO2Ext, data = payload, headers = headers)
   CO2 = str(CO2ExtObject.text)

   #2- poster vers producer pour post sur kafka>topicCO2Extracted
   topicName = topicNameCo2Extracted
   headers = {"HTTP_HOST": "MyVeryOwnHost", "topicName": topicName, "contentType": 'text/plain' }
   urlProduc = 'http://localhost:5001/messageBroker'
#   urlProduc = 'http://co22tok.westeurope.cloudapp.azure.com:5001/messageBroker'
   COProd = requests.post(url = urlProduc, data = CO2, headers = headers)
   print("valeur traitee de CO22 envoyee de orchestre vers producer : ", CO2, topicName)
   return("CO2")

  elif "topicCO2Kafka" in source:

   payload = request.data
#   payload = payload.decode("utf-8")
   print("payload recu de consumer2 ", payload)
   headers = {"HTTP_HOST": "postMessageToExtractValue" }
#   urlCO2Json = 'http://localhost:5005/CO2Json2Blockchain'
        #  urlCO2Json = 'http://co22tok.westeurope.cloudapp.azure.com:5005/CO2Json2Blockchain'
#   CO2Json4Blockchain = requests.post(url = urlCO2Json, data = payload, headers = headers)
#   CO2 = CO2Json4Blockchain.text
   print("j'ai recupere CO2 du formateur pour blockchain", CO2)
   return(CO2)
#   headers = {"HTTP_HOST": "postMessageToExtractValue" }
#   urlCO2Json = 'http://13.81.97.209:8545'
#   CO2Json4Blockchain = requests.post(url = urlCO2Json, data = CO2)    #, headers = headers)
#   CO2 = CO2Json4Blockchain.text


#  return(CO2)

  #1) recup val co2
  #2) envoi par post sur BC
  #3) envoi par post sur outil gestion de tâches

  else:
   print("C parti vers l'etoile noire")
   headers = {"HTTP_HOST": "MyVeryOwnHost", "topicName": topicNamePending, "contentType": 'text/plain' }
   urlProduc = 'http://co22tok.westeurope.cloudapp.azure.com:5001/messageBroker'
   COProd = requests.post(url = urlProduc, data = payload, headers = headers)
   print("valeur recue invalide : ", payload)
   return("CO2")
   return("request source unknwon")

 except:
  print("nous allons vers le cote obscure de la force")
  return("bye!")

if __name__ == '__main__':
 app.run(debug=False,port=5000, host='0.0.0.0')
