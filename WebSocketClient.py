# encoding: utf-8
"""
@author: liuyun
@time: 2019/1/29/029 10:41
@desc:
"""
import requests
import websocket
import json

class WebSocketClient():

    def __init__(self, ip, port):
        websocket.enableTrace(True)
        self.ip = ip
        self.port = port
        self.clientId = ""
        self.clientHander = None
        self.requestHandler = None
        self.ws = websocket.WebSocketApp("ws://{}:{}/_mockserver_callback_websocket".format(self.ip, self.port),
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)


    def on_message(self, msg):
        body = json.loads(msg)

        if body['type'] == "org.mockserver.model.HttpRequest":
            request = json.loads(body['value'])

            value = {"headers": [
                                    {
                                        "name": "WebSocketCorrelationId",
                                        "values": request['headers']["WebSocketCorrelationId"]
                                    }
                                ],
                     "statusCode": 200,
                     "body": json.dumps(self.requestHandler(request))
                    }

            respond = {"type": "org.mockserver.model.HttpResponse",
                       "value": json.dumps(value)
                       }
            self.ws.send(json.dumps(respond))

        if body['type'] == "org.mockserver.serialization.model.WebSocketClientIdDTO":
            registration = json.loads(body['value'])
            if registration['clientId']:
                self.clientId = registration['clientId']
                if (self.clientHander):
                    content = self.clientHander(self.clientId)
                    print(content)
                    requests.put("http://{ip}:{port}/expectation".format(ip=self.ip, port=self.port), json=content)

    def on_error(self, error):
        print(error)


    def on_close(self):
        print("### closed ###")

    def on_open(self):
        pass

    def run(self):
        self.ws.run_forever()

    def clientIdCallback(self, callback):
        self.clientIdHandler = callback;
        if self.clientId:
            self.clientIdHandler(self.clientId);

    def requesCallback(self, callback):
        self.requestHandler = callback;

