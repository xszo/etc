def o(line=''):
    out.write(line + '\n')


o('[General]')
o('update-url = ' + src['base'] + 'other/shadowrocket.conf')
o('hijack-dns = *:53')
o('dns-server = system, ' + src['dns']['https'])
o()
o('[Proxy Group]')
for item in src['node']:
    line = item['name'] + ' = '
    if item['type'] == 'static':
        line += 'select'
    elif item['type'] == 'test':
        line += 'url-test, url=' + src['t-http']
    else:
        continue
    if isinstance(item['content'], list):
        for val in item['content']:
            line += (', ' + val)
    else:
        line += ', policy-regex-filter=' + item['content']
    o(line)
o()
o('[Rule]')
for item in src['filter']:
    match item[0]:
        case 0:
            o('FINAL, ' + item[1])
        case 1:
            o('DOMAIN-SUFFIX, ' + item[1] + ', ' + item[2])
        case 2:
            o('DOMAIN, ' + item[1] + ', ' + item[2])
        case 3:
            o('IP-CIDR, ' + item[1] + ', ' + item[2])
        case 4:
            o('IP-CIDR6, ' + item[1] + ', ' + item[2])
        case 5:
            o('GEOIP, ' + item[1] + ', ' + item[2])
