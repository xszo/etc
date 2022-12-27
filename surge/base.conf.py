with open('var/main.yml', 'tr', encoding='utf-8') as file:
    src = yaml.safe_load(file)
base = src['meta']['base'] + 'surge/'
interval = str(src['meta']['interval'])

def o(line=''):
    out.write(line + '\n')

# start

o('#!MANAGED-CONFIG ' + base + 'base.conf' + ' interval=' + interval + ' strict=false')
o()
o('[General]')
o('loglevel = warning')
o('hijack-dns = *:53')
o('dns-server = system')
o('internet-test-url = ' + src['meta']['t-http'])
o('proxy-test-url = ' + src['meta']['t-http'])
o()
o('[Proxy Group]')
for item in src['node']:
    line = item['name'] + ' = '
    if item['type'] == 'static':
        line += 'select'
    elif item['type'] == 'test':
        line += 'url-test'
    else:
        continue
    if isinstance(item['content'], list):
        for val in item['content']:
            line += (', ' + val)
    else:
        line += ', include-all-proxies=true'
        if not item['content'] == '-a':
            line += ', policy-regex-filter=' + item['content']
    o(line)
o()
o('[Rule]')
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'domain' in item['type']:
            o('RULE-SET, ' + base + item['content'] + '.txt, ' +
              item['name'] + ', update-interval=' + interval)
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'ipcidr' in item['type']:
            o('RULE-SET, ' + base + item['content'] + '.ip.txt, ' +
              item['name'] + ', update-interval=' + interval)
for item in src['filter']:
    if not isinstance(item['type'], list):
        if item['type'] == 'geoip':
            o('GEOIP, ' + item['content'] + ', ' + item['name'])
        elif item['type'] == 'final':
            o('FINAL, ' + item['name'])
