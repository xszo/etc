def o(line):
    out.write(line + '\n')


o('#!MANAGED-CONFIG ' + src['base'] + 'surge/base.conf' +
  ' interval=' + str(src['interval']) + ' strict=false')
o('''[General]
loglevel=warning
hijack-dns=*:53
udp-policy-not-supported-behaviour=REJECT''')
o('dns-server=' + src['dns']['plain'][0] + ',' + src['dns']['plain'][1])
o('encrypted-dns-server=' + src['dns']['doh'])
o('internet-test-url=' + src['t-http'])
o('proxy-test-url=' + src['t-http'])
o('[Proxy Group]')
for item in src['node']:
    line = item['name'] + '='
    if item['type'] == 'static':
        line += 'select'
    elif item['type'] == 'test':
        line += 'url-test'
    else:
        continue
    if isinstance(item['content'], list):
        for val in item['content']:
            line += (',' + val)
    else:
        line += ',include-all-proxies=true,policy-regex-filter=' + \
            item['content']
    o(line)
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
