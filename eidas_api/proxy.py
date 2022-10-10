#!/usr/bin/env python
from flask import Flask, request, abort, jsonify
import requests
import jwt
import re
import socket

private_key = open('new_key').read()
public_key = open('new_key.pub').read()

app = Flask(__name__)

@app.route('/SP', methods=['POST'])
def handle_push():
    if 'AnsibleTower' in request.headers and request.headers['AnsibleTower'] == 'xSecretx':
        # Trigger some other external action
        print("Request dictionary: {}".format(request.json))
        return jsonify({'status': 'triggered'}), 201
    #print (request.form)
    data_form = {}

    for fieldname, value in request.form.items():
        data_form[fieldname] = value

    #print (data_form)
    response = requests.post("http://10.10.11.9:8080/IdP/Response", data=data_form)
    #print (response.content)
    success = re.search(r'"created_on(.*?)</textarea>', response.text, re.S)
    print (response.text)
    print (success.group())

    attributes = re.search(r'^.*<\/noscript', response.text, re.S)

    token3 = jwt.encode({'data3': attributes.group()}, private_key, algorithm='RS256').decode('utf-8')

    token2 = jwt.encode({'data2': success.group()}, private_key, algorithm='RS256').decode('utf-8')

    token = jwt.encode({'attributes': token3, 'assertion': token2}, private_key, algorithm='RS256').decode('utf-8')

    payload = jwt.decode(token, public_key, algorithms=['RS256'])
    payload2 = jwt.decode(token2, public_key, algorithms=['RS256'])
    payload3 = jwt.decode(token3, public_key, algorithms=['RS256'])
    return token, 200

if __name__ == '__main__':
    print("Listening...")
    app.run(debug=True, host='0.0.0.0', port=8079)
