def o(line):
    out.write(line + '\n')


o('# ' + src['base'] + 'clash/scv.ini')
o('[custom]')
o('clash_rule_base=' + src['base'] + 'clash/scv.yml')
for item in src['node']:
    line = 'custom_proxy_group=' + item['name']
    if item['type'] == 'static':
        line += '`select'
    elif item['type'] == 'test':
        line += '`url-test'
    else:
        continue
    if isinstance(item['content'], list):
        for val in item['content']:
            line += ('`[]' + val)
    else:
        line += '`' + item['content']
    if item['type'] == 'test':
        line += '`' + src['t-http'] + '`600'
    o(line)
o('enable_rule_generator=true')
o('overwrite_original_rules=true')
for item in src['filter']:
    match item[0]:
        case 0:
            o('ruleset=' + item[1] + ',[]FINAL')
        case 1:
            o('ruleset=' + item[2] + ',[]DOMAIN-SUFFIX,' + item[1])
        case 2:
            o('ruleset=' + item[2] + ',[]DOMAIN,' + item[1])
        case 3:
            o('ruleset=' + item[2] + ',[]IP-CIDR,' + item[1])
        case 4:
            o('ruleset=' + item[2] + ',[]IP-CIDR6,' + item[1])
        case 5:
            o('ruleset=' + item[2] + ',[]GEOIP,' + item[1])
