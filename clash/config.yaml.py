with open('var/main.yml', 'tr', encoding='utf-8') as file:
    src = yaml.safe_load(file)
base = src['meta']['base'] + 'clash/'
interval = str(src['meta']['interval'])


def o(line=''):
    out.write(line + '\n')


o('# ' + base + 'config.yaml' + '''\n
log-level: silent
mode: rule
profile:
  store-selected: true
  store-fake-ip: true

mixed-port: 8421
redir-port: 8422
allow-lan: false
external-controller: 127.0.0.1:8420
secret: 00000000
tun:
  enable: true
  stack: gvisor
  dns-hijack: [198.18.0.2:53]
  auto-route: true
  auto-detect-interface: true

dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter:
    - +.lan
    - +.local
  default-nameserver:
    - 1.1.1.1
    - 1.0.0.1
  nameserver:
  - https://cloudflare-dns.com/dns-query''')
o()
o('proxy-groups:')
for item in src['node']:
    tmp = '- name: ' + item['name']
    if item['type'] == 'static':
        tmp += '\n  type: select'
    elif item['type'] == 'test':
        tmp += '\n  type: url-test'
        tmp += '\n  lazy: true'
        tmp += '\n  url: ' + src['meta']['t-http']
    else:
        continue
    if isinstance(item['content'], list):
        tmp += '\n  proxies:'
        for val in item['content']:
            tmp += ('\n  - ' + val)
    else:
        tmp += '\n  filter: '
        if item['content'] == '-a':
            tmp += '.*'
        else:
            tmp += item['content']
    o(tmp)
o()
o('rule-providers:')
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'domain' in item['type']:
            o('  ' + item['name'] + ':')
            o('    behavior: domain')
            o('    type: http')
            o('    url: ' + base + 'filter/' + item['name'] + '.yml')
            o('    interval: ' + interval)
            o('    path: ./' + 'filter/' + item['name'] + '.yml')
        if 'ipcidr' in item['type']:
            o('  ' + item['name'] + '.ip:')
            o('    behavior: ipcidr')
            o('    type: http')
            o('    url: ' + base + 'filter/' + item['name'] + '.ip.yml')
            o('    interval: ' + interval)
            o('    path: ./' + 'filter/' + item['name'] + '.ip.yml')
o()
o('rules:')
for item in src['filter']:
    if isinstance(item['type'], list) and 'domain' in item['type']:
        o('- RULE-SET, ' + item['name'] + ', ' + item['content'])
for item in src['filter']:
    if isinstance(item['type'], list) and 'ipcidr' in item['type']:
        o('- RULE-SET, ' + item['name'] + '.ip, ' + item['content'])
for item in src['filter']:
    if not isinstance(item['type'], list):
        if item['type'] == 'geoip':
            o('- GEOIP, ' + item['name'] + ', ' + item['content'])
        elif item['type'] == 'final':
            o('- FINAL, ' + item['content'])
