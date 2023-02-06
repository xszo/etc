import os

tmpPath = 'tmp/net/filter'
if os.path.exists(tmpPath):
    os.system('rm -Rf ' + tmpPath)
os.makedirs(tmpPath)
os.system('cp -Rf src/* ' + tmpPath)
