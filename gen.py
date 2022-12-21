import os
import yaml

genPath = 'gen/net/'
listSrc = [
    'quantumult/profile.conf',
    'clash/config.yaml', 'clash/scv.ini', 'clash/scv.yml',
    'surge/profile.conf', 'surge/base.conf', 'surge/router.sgmodule',
    'other/scv.ini', 'other/sr.conf'
]

# call generator

for srcPath in listSrc:
    outPath = genPath + srcPath
    outDir = os.path.dirname(outPath)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    if os.path.exists(srcPath):
        os.system('cp -f ' + srcPath + ' ' + outPath)
    else:
        exe = open(srcPath + '.py', 'tr', encoding='utf-8')
        out = open(outPath, 'tw', encoding='utf-8')
        exec(exe.read())
        exe.close()
        out.close()
