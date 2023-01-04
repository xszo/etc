with open('var/main.yml', 'tr', encoding='utf-8') as file:
    src = yaml.safe_load(file)
with open('var/cn.yml', 'tr', encoding='utf-8')as file:
    scn = yaml.safe_load(file)
base = src['meta']['base']
interval = str(src['meta']['interval'])


def o(line=''):
    out.write(line + '\n')


o('[General]')
o('update-url = ' + base + 'other/sr.conf')
o('hijack-dns = *:53')
o('dns-server = system')
o()
o('[Proxy Group]')
for item in scn['node']:
    line = item['name'] + ' = '
    if item['type'] == 'static':
        line += 'select'
    elif item['type'] == 'test':
        line += 'url-test, url=' + src['meta']['t-http']
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
for item in scn['filter']:
    if isinstance(item['type'], list) and 'domain' in item['type']:
        o('RULE-SET, ' + base + 'surge/filter/' +
          item['name'] + '.txt, ' + item['content'])
for item in scn['filter']:
    if isinstance(item['type'], list) and 'ipcidr' in item['type']:
        o('RULE-SET, ' + base + 'surge/filter/' +
          item['name'] + '.ip.txt, ' + item['content'])
for item in scn['filter']:
    if not isinstance(item['type'], list):
        if item['type'] == 'geoip':
            o('GEOIP, ' + item['name'] + ', ' + item['content'])
        elif item['type'] == 'final':
            o('FINAL, ' + item['content'])
