import yaml

with open('clash/base.yml', 'tr', encoding='utf-8') as file:
    raw = yaml.safe_load(file)
raw['dns']['default-nameserver'] = src['dns']['plain']
raw['dns']['nameserver'] = [src['dns']['https']]

raw['proxy-groups'] = []
for item in src['node']:
    line = {'name': item['name']}
    if item['type'] == 'static':
        line['type'] = 'select'
    elif item['type'] == 'test':
        line.update({
            'type': 'url-test',
            'lazy': True,
            'interval': 600,
            'url': src['t-http']})
    else:
        continue
    if isinstance(item['content'], list):
        line['proxies'] = item['content']
    else:
        line['include-all'] = True
        line['filter'] = item['content']
    raw['proxy-groups'].append(line)

raw['rules'] = []
for item in src['filter']:
    match item[0]:
        case 0:
            raw['rules'].append('MATCH,' + item[1])
        case 1:
            raw['rules'].append('DOMAIN-SUFFIX,' + item[1] + ',' + item[2])
        case 2:
            raw['rules'].append('DOMAIN,' + item[1] + ',' + item[2])
        case 3:
            raw['rules'].append('IP-CIDR,' + item[1] + ',' + item[2])
        case 4:
            raw['rules'].append('IP-CIDR6,' + item[1] + ',' + item[2])
        case 5:
            raw['rules'].append('GEOIP,' + item[1] + ',' + item[2])

yaml.safe_dump(raw, out)
