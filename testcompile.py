import py_compile
import os

py_compile.compile('cc_server/chat_server.py', cfile='bin/chat_server.pyc')
py_compile.compile('cc_client/chat_client.py', cfile='bin/chat_client.pyc')

#uncomment to remove pyc files on compile
#for fileName in os.listdir('bin/'):
#    os.remove('bin/' + fileName)
