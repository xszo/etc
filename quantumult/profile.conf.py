def o(line=''):
    out.write(line + '\n')


o('[general]')
o('network_check_url = ' + src['t-http'])
o('server_check_url = ' + src['t-http'])
o('resource_parser_url = ' + src['base'] + 'quantumult/parser.js')
o()
o('[dns]')
o('no-system')
for item in src['dns']['plain']:
    o('server = ' + item)
o('doh-server = ' + src['dns']['https'])
o()
o('[mitm]')
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
        line += ', server-tag-regex=' + item['content']
    o(line + ', img-url=' + item['a-ico'])
o()
o('[filter_local]')
for item in src['filter']:
    if item[0] == 0:
        o('final, ' + item[1])
o('[filter_remote]')
o(src['base'] + 'quantumult/' + src['x'] +
  'filter.txt, update-interval=' + str(src['interval']))
o()
o('[rewrite_local]')
o('[rewrite_remote]')
o()
o('[server_local]')
o('[server_remote]')
