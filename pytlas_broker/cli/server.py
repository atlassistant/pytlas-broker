import os
from pytlas_broker.conversing import Server
from pytlas_broker.conversing.agents import FromFileFactory
from pytlas_broker.communicating.mqtt import MQTTChannel

def main():
    serv = Server(FromFileFactory(os.getcwd()))
    with MQTTChannel('mqtt.eclipse.org') as mqtt:
        mqtt.attach(serv)

        input('Type anything to stop')

# serv = Server()

# with GSMChannel() as gsm:
#   with MQTTChannel() as mqtt:
#     gsm.attach(serv)
#     mqtt.attach(serv)