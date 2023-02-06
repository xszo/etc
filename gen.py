import os

TmpPath = 'tmp/net/filter'
if os.path.exists(TmpPath):
    os.system('rm -Rf ' + TmpPath)
os.makedirs(TmpPath)
os.system('cp -Rf src/* ' + TmpPath)
