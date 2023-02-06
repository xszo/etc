def o(line):
    out.write(line + '\n')


o('# ' + src['base'] + 'quantumult/profile.conf')
o('[general]')
o('network_check_url=' + src['t-http'])
o('server_check_url=' + src['t-http'])
o('resource_parser_url=' + src['base'] + 'quantumult/parser.js')
o('[dns]')
o('no-system')
o('server=' + src['dns']['plain'][0])
o('server=' + src['dns']['plain'][1])
o('doh-server=' + src['dns']['doh'])
o('[policy]')
for item in src['node']:
    if item['type'] == 'static':
        line = 'static='
    elif item['type'] == 'test':
        line = 'url-latency-benchmark='
    else:
        continue
    line += item['name']
    if isinstance(item['content'], list):
        for val in item['content']:
            line += (',' + val)
    else:
        line += ',server-tag-regex=' + item['content']
    o(line + ',img-url=' + item['a-ico'])
o('[filter_local]')
for item in src['filter']:
    if item[0] == 0:
        o('final,' + item[1])
o('[filter_remote]')
o(src['base'] + 'quantumult/filter.txt,update-interval=' + str(src['interval']))
o('[mitm]')
o('[rewrite_local]')
o('[rewrite_remote]')
o('[server_local]')
o('[server_remote]')
