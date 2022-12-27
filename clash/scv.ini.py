with open('var/main.yml', 'tr', encoding='utf-8') as file:
    src = yaml.safe_load(file)
base = src['meta']['base'] + 'clash/'
interval = str(src['meta']['interval'])

def o(line=''):
    out.write(line + '\n')

# start

o('# ' + base + 'scv.ini')
o('[custom]')
o('clash_rule_base=' + base + 'scv.yml')
o('add_emoji=false')
o('remove_old_emoji=false')
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
        if item['content'] == '-a':
            line += '`.*'
        else:
            line += '`' + item['content']
    if item['type'] == 'test':
        line += '`' + src['meta']['t-http'] + '`600'
    o(line)
o('enable_rule_generator=true')
o('overwrite_original_rules=true')
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'domain' in item['type']:
            o('ruleset=' + item['name'] + ',clash-domain:' +
              base + item['content'] + '.yml')
for item in src['filter']:
    if isinstance(item['type'], list):
        if 'ipcidr' in item['type']:
            o('ruleset=' + item['name'] + ',clash-ipcidr:' +
              base + item['content'] + '.ip.yml')
for item in src['filter']:
    if not isinstance(item['type'], list):
        if item['type'] == 'geoip':
            o('ruleset=' + item['name'] + ',[]GEOIP,' + item['content'])
        elif item['type'] == 'final':
            o('ruleset=' + item['name'] + ',[]FINAL')
