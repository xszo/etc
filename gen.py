import os
import yaml

genPath = 'gen/net/'
listDir = [
    'quantumult/filter/',
    'clash/filter/',
    'surge/filter/'
]
listFilter = [
    'direct',
    'global', 'system', 'block',
    'region', 'r-cn', 'r-jp', 'r-tw', 'r-us'
]

# create path

for outDir in listDir:
    outDir = genPath + outDir
    if not os.path.exists(outDir):
        os.makedirs(outDir)

# generate filter

for item in listFilter:
    with open('filter/' + item + '.yml', 'tr', encoding='utf-8') as file:
        src = yaml.safe_load(file)
    flagDomain = 'domain' in src
    flagIp = 'ip' in src
    flagIp6 = 'ip6' in src
    flagPort = 'port' in src

    # generate quantumult conf

    with open(genPath + listDir[0] + item + '.txt', 'tw', encoding='utf-8') as out:
        if flagDomain:
            for line in src['domain']:
                if line[0] == '_':
                    out.write('host,' + line[1:] + ',proxy\n')
                else:
                    out.write('host-suffix,' + line + ',proxy\n')
        if flagIp:
            for line in src['ip']:
                out.write('ip-cidr,' + line + ',proxy\n')
        if flagIp6:
            for line in src['ip6']:
                out.write('ip6-cidr,' + line + ',proxy\n')

    # generate clash conf

    outDir = genPath + listDir[1]
    if flagDomain:
        with open(outDir + item + '.yml', 'tw', encoding='utf-8') as out:
            out.write('payload:\n')
            for line in src['domain']:
                if line[0] == '_':
                    out.write('- ' + line[1:] + '\n')
                else:
                    out.write('- +.' + line + '\n')
    if flagIp or flagIp6:
        with open(outDir + item + '.ip.yml', 'tw', encoding='utf-8') as out:
            out.write('payload:\n')
            if flagIp:
                for line in src['ip']:
                    out.write('- ' + line + '\n')
            if flagIp6:
                for line in src['ip6']:
                    out.write('- ' + line + '\n')
    if flagPort:
        with open(outDir + item + '.ms.yml', 'tw', encoding='utf-8') as out:
            out.write('payload:\n')
            for line in src['port']:
                out.write('- DST-PORT,' + line + '\n')

    # generate surge conf

    outDir = genPath + listDir[2]
    if flagDomain:
        with open(outDir + item + '.txt', 'tw', encoding='utf-8') as out:
            for line in src['domain']:
                if line[0] == '_':
                    out.write('DOMAIN,' + line[1:] + '\n')
                else:
                    out.write('DOMAIN-SUFFIX,' + line + '\n')
    if flagIp or flagIp6:
        with open(outDir + item + '.ip.txt', 'tw', encoding='utf-8') as out:
            if flagIp:
                for line in src['ip']:
                    out.write('IP-CIDR,' + line + '\n')
            if flagIp6:
                for line in src['ip6']:
                    out.write('IP-CIDR6,' + line + '\n')
    if flagPort:
        with open(outDir + item + '.ms.txt', 'tw', encoding='utf-8') as out:
            for line in src['port']:
                out.write('DEST-PORT,' + line + '\n')
