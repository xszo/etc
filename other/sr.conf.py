with open('var/main.yml', 'tr', encoding='utf-8') as file:
    sb = yaml.safe_load(file)
with open('var/mini.yml', 'tr', encoding='utf-8')as file:
    src = yaml.safe_load(file)
base = sb['meta']['base']
interval = str(sb['meta']['interval'])

def o(line=''):
    out.write(line + '\n')

# start

o('[General]')
o('update-url = ' + base + 'other/sr.conf')
o('hijack-dns = *:53')
o('dns-server = system')
o()
o('[Proxy Group]')
for item in src['node']:
    line = item['name'] + ' = '
    if item['type'] == 'static':
        line += 'select'
    elif item['type'] == 'test':
        line += 'url-test, url=' + sb['meta']['t-http']
    else:
        continue
    if isinstance(item['content'], list):
        for val in item['content']:
            line += (', ' + val)
    else:
        if item['content'] == '-a':
            line += ', policy-regex-filter=.*'
        else:
            line += ', policy-regex-filter=' + item['content']
    o(line)
o()
o('[Rule]')
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'domain' in item['type']:
            o('RULE-SET, ' + base + 'surge/' + item['content'] + '.txt, ' + item['name'])
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'ipcidr' in item['type']:
            o('RULE-SET, ' + base + 'surge/' + item['content'] + '.ip.txt, ' + item['name'])
for item in src['filter']:
    if not isinstance(item['type'], list):
        if item['type'] == 'geoip':
            o('GEOIP, ' + item['content'] + ', ' + item['name'])
        elif item['type'] == 'final':
            o('FINAL, ' + item['name'])
