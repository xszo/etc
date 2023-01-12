import requests
import os
import yaml

genPath = 'gen/net/'
listExec = [
    'quantumult/profile.conf', 'quantumult/filter.txt',
    'clash/config.yaml', 'clash/scv.ini',
    'surge/profile.conf', 'surge/base.conf', 'surge/router.sgmodule',
    'other/scv.ini'
]
listExt = [
    'quantumult/parser.js https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/resource-parser.js'
]

# load src

with open('src/main.yml', 'tr', encoding='utf-8') as file:
    src = yaml.safe_load(file)
with open('src/node.yml', 'tr', encoding='utf-8') as file:
    src['node'] = yaml.safe_load(file)

# load filter

src['filter'] = []
srcDomain = [[], [], [], []]
with open('src/filter.yml', 'tr', encoding='utf-8') as file:
    listFilter = yaml.safe_load(file)
for item in listFilter:
    if item['type'] == 'gen':
        with open('tmp/filter/' + item['name'] + '.yml', 'tr', encoding='utf-8') as file:
            raw = yaml.safe_load(file)
        content = item['content']
        if 'domain' in raw:
            for line in raw['domain']:
                if line[0] == '_':
                    srcDomain[line.count('.')].append([2, line[1:], content])
                else:
                    srcDomain[line.count('.')].append([1, line, content])
        if 'ipcidr' in raw:
            for line in raw['ipcidr']:
                if line[0] == '[':
                    src['filter'].append([4, line[1:-1], content])
                else:
                    src['filter'].append([3, line, content])
    elif item['type'] == 'geoip':
        src['filter'].append([5, item['name'], item['content']])
    elif item['type'] == 'final':
        src['filter'].append([0, item['content']])
for item in srcDomain:
    src['filter'] = item + src['filter']

# call generator

for exePath in listExec:
    outPath = genPath + exePath
    outDir = os.path.dirname(outPath)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    if os.path.exists(exePath):
        os.system('cp -f ' + exePath + ' ' + outPath)
    else:
        exe = open(exePath + '.py', 'tr', encoding='utf-8')
        out = open(outPath, 'tw', encoding='utf-8')
        exec(exe.read(), {'out': out, 'src': src})
        exe.close()
        out.close()

# fetch external

for item in listExt:
    item = (genPath + item).split(' ')
    with open(item[0], 'tw', encoding='utf-8') as file:
        file.write(requests.get(item[1]).text)
