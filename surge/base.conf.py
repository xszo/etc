def o(line=''):
    out.write(line + '\n')


base = src['base'] + 'surge/'
interval = str(src['interval'])

o('#!MANAGED-CONFIG ' + base + 'base.conf' +
  ' interval=' + interval + ' strict=false')
o()
o('[General]')
o('loglevel = warning')
o('hijack-dns = *:53')
o('dns-server = ' + src['dns']['plain'][0] + ', ' + src['dns']['plain'][1])
o('encrypted-dns-server = ' + src['dns']['doh'])
o('internet-test-url = ' + src['t-http'])
o('proxy-test-url = ' + src['t-http'])
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
    if 'content' in item:
        if isinstance(item['content'], list):
            for val in item['content']:
                line += (', ' + val)
        else:
            line += ', include-all-proxies=true, policy-regex-filter=' + \
                item['content']
    else:
        line += ', include-all-proxies=true'
    o(line)
o()
o('[Rule]')
for item in src['filter']:
    match item[0]:
        case 0:
            o('FINAL,' + item[1])
        case 1:
            o('DOMAIN-SUFFIX,' + item[1] + ',' + item[2])
        case 2:
            o('DOMAIN,' + item[1] + ',' + item[2])
        case 3:
            o('IP-CIDR,' + item[1] + ',' + item[2])
        case 4:
            o('IP-CIDR6,' + item[1] + ',' + item[2])
        case 5:
            o('GEOIP,' + item[1] + ',' + item[2])
