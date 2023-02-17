import requests
import os
import yaml

ListSrc = ['src/main.yml', 'src/mini.yml']
ListExt = [
    'quantumult/parser.js https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/resource-parser.js'
]

# ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- # ---- #

GenPath = 'out/net/'
ListGen = {
    'quantumult': ['quantumult/profile.conf', 'quantumult/filter.txt'],
    'clash': ['clash/base.yml', 'clash/config.yaml', 'clash/scv.ini'],
    'surge': ['surge/base.conf', 'surge/profile.conf', 'surge/router.sgmodule', 'other/scv.ini'],
    'shadowrocket': ['other/shadowrocket.conf']
}

# generate

for unit in ListSrc:
    with open('src/base.yml', 'tr', encoding='utf-8') as file:
        src = yaml.safe_load(file)

    # load src
    with open(unit, 'tr', encoding='utf-8') as file:
        src.update(yaml.safe_load(file))
    srcX = src['x']
    src['x'] = srcX['alias']
    if 'include' in srcX:
        for key, val in srcX['include'].items():
            with open(val, 'tr', encoding='utf-8') as file:
                src[key] = yaml.safe_load(file)

    # load filter
    ListFilter = src['filter']
    src['filter'] = []
    SrcDomain = [[], [], [], []]
    for item in ListFilter:
        if item['type'] == 'gen':
            with open('tmp/net/filter/' + item['name'] + '.yml', 'tr', encoding='utf-8') as file:
                raw = yaml.safe_load(file)
            if 'domain' in raw:
                for line in raw['domain']:
                    if line[0] == '_':
                        SrcDomain[line.count('.')].append(
                            (2, line[1:], item['content']))
                    else:
                        SrcDomain[line.count('.')].append(
                            (1, line, item['content']))
            if 'ipcidr' in raw:
                for line in raw['ipcidr']:
                    if line[0] == '[':
                        src['filter'].append((4, line[1:-1], item['content']))
                    else:
                        src['filter'].append((3, line, item['content']))
    for item in SrcDomain:
        src['filter'] = item + src['filter']
    for item in ListFilter:
        if item['type'] == 'geoip':
            src['filter'].append((5, item['name'], item['content']))
    for item in ListFilter:
        if item['type'] == 'final':
            src['filter'].append((0, item['content']))

    # call generator
    for item in srcX['gen']:
        for exePath in ListGen[item]:
            outDir = GenPath + os.path.dirname(exePath)
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            if os.path.exists(exePath):
                outPath = GenPath + exePath
                if not os.path.exists(outPath):
                    os.system('cp -f ' + exePath + ' ' + outPath)
            else:
                outPath = os.path.join(
                    outDir, srcX['alias'] + os.path.basename(exePath))
                if not os.path.exists(outPath):
                    exe = open(exePath + '.py', 'tr', encoding='utf-8')
                    out = open(outPath, 'tw', encoding='utf-8')
                    exec(exe.read(), {'out': out, 'src': src})
                    exe.close()
                    out.close()

# fetch external

for item in ListExt:
    item = (GenPath + item).split(' ')
    with open(item[0], 'tw', encoding='utf-8') as file:
        file.write(requests.get(item[1]).text)
