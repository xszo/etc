def o(line):
    out.write(line + '\n')


o('# ' + src['base'] + 'clash/config.yaml' + '''
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
  - ''' + src['dns']['plain'][0] + '''
  - ''' + src['dns']['plain'][1] + '''
  nameserver:
  - ''' + src['dns']['doh'])
o('proxy-groups:')
for item in src['node']:
    line = '- name: ' + item['name']
    if item['type'] == 'static':
        line += '\n  type: select'
    elif item['type'] == 'test':
        line += '\n  type: url-test'
        line += '\n  lazy: true'
        line += '\n  url: ' + src['t-http']
    else:
        continue
    if isinstance(item['content'], list):
        line += '\n  proxies:'
        for val in item['content']:
            line += ('\n  - ' + val)
    else:
        line += '\n  filter: ' + item['content']
    o(line)
o('rules:')
for item in src['filter']:
    match item[0]:
        case 0:
            o('- MATCH,' + item[1])
        case 1:
            o('- DOMAIN-SUFFIX,' + item[1] + ',' + item[2])
        case 2:
            o('- DOMAIN,' + item[1] + ',' + item[2])
        case 3:
            o('- IP-CIDR,' + item[1] + ',' + item[2])
        case 4:
            o('- IP-CIDR6,' + item[1] + ',' + item[2])
        case 5:
            o('- GEOIP,' + item[1] + ',' + item[2])
