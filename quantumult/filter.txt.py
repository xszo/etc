def o(line):
    out.write(line + '\n')


for item in src['filter']:
    match item[0]:
        case 0:
            o('final,' + item[1])
        case 1:
            o('host-suffix,' + item[1] + ',' + item[2])
        case 2:
            o('host,' + item[1] + ',' + item[2])
        case 3:
            o('ip-cidr,' + item[1] + ',' + item[2])
        case 4:
            o('ip6-cidr,' + item[1] + ',' + item[2])
        case 5:
            o('geoip,' + item[1] + ',' + item[2])
