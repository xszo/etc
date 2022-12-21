import requests
import os

listSrc = [
    'net/quantumult/parser.js https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/resource-parser.js'
]

for item in listSrc:
    item = ('gen/' + item).split(' ')
    os.makedirs(os.path.dirname(item[0]))
    with open(item[0], 'tw', encoding='utf-8') as file:
        file.write(requests.get(item[1]).text)
