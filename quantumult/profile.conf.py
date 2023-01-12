def o(line=''):
    out.write(line + '\n')


base = src['base'] + 'quantumult/'
interval = str(src['interval'])

o('# ' + base + 'profile.conf')
o()
o('[general]')
o('network_check_url = ' + src['t-http'])
o('server_check_url = ' + src['t-http'])
o('resource_parser_url = ' + base + 'parser.js')
o()
o('[dns]')
o('no-system')
o('server = ' + src['dns']['plain'][0])
o('server = ' + src['dns']['plain'][1])
o('doh-server = ' + src['dns']['doh'])
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
    if 'content' in item:
        if isinstance(item['content'], list):
            for val in item['content']:
                line += (', ' + val)
        else:
            line += ', server-tag-regex=' + item['content']
    else:
        line += ', server-tag-regex=.*'
    o(line + ', img-url=' + item['a-ico'])
o()
o('[filter_local]')
for item in src['filter']:
    if item[0] == 0:
        o('final, ' + item[1])
o()
o('[filter_remote]')
o(base + 'filter.txt, tag=filter, update-interval=' + interval)
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
