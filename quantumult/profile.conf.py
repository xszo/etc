with open('var/main.yml', 'tr', encoding='utf-8') as file:
    src = yaml.safe_load(file)
base = src['meta']['base'] + 'quantumult/'
interval = str(src['meta']['interval'])

def o(line=''):
    out.write(line + '\n')

# start

o('# ' + base + 'profile.conf')
o()
o('[general]')
o('network_check_url = ' + src['meta']['t-http'])
o('server_check_url = ' + src['meta']['t-http'])
o('resource_parser_url = ' + base + 'parser.js')
o()
o('[dns]')
o()
o('[policy]')
for item in src['node']:
    if item['type'] == 'static':
        line = 'static = '
    elif item['type'] == 'test':
        line = 'url-latency-benchmark = '
    else:
        continue
    line += item['name']
    if isinstance(item['content'], list):
        for val in item['content']:
            line += (', ' + val)
    else:
        line += ', server-tag-regex='
        if item['content'] == '-a':
            line += '.*'
        else:
            line += item['content']
    o(line + ', img-url=' + item['a-ico'])
o()
o('[filter_local]')
o('host-suffix, quantumult.app, _GLOBAL')
for item in src['filter']:
    if not isinstance(item['type'], list):
        if item['type'] == 'geoip':
            o('geoip, ' + item['content'] + ', ' + item['name'])
        elif item['type'] == 'final':
            o('final, ' + item['name'])
o()
o('[filter_remote]')
for item in src['filter']:
    if isinstance(item['type'], list):
        o(base + item['content'] + '.txt, tag=' + item['content'] +
          ', force-policy=' + item['name'] + ', update-interval=' + interval)
o()
o('[mitm]')
o()
o('[rewrite_local]')
o()
o('[rewrite_remote]')
o()
o('[server_local]')
o()
o('[server_remote]')
