import os

path = 'tmp/filter'
if os.path.exists(path):
    os.system('rm -Rf ' + path)
os.makedirs(path)
os.system('cp -Rf src/* ' + path + '/')
