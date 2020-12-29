from __future__ import print_function
from xmlrpclib import ServerProxy

SERVER = 'http://localhost:8072'
DATABASE = 'db1'
USERNAME = 'admin'
PASSWORD = 'david777'

server = ServerProxy('http://localhost:8072/xmlrpc/common')
user_id = server.login(DATABASE, USERNAME, PASSWORD)

server = ServerProxy('http://localhost:8072/xmlrpc/object')

user_ids = server.execute(
    DATABASE, user_id, PASSWORD,
    'res.users', 'search', []
)

users = server.execute(
    DATABASE, user_id, PASSWORD,
    'res.users', 'read', user_ids, []
)

for user in users:
    print(user['id'], user['name'])

invoice_ids = server.execute(
    DATABASE, user_id, PASSWORD, 'account.invoice', search, re[])
