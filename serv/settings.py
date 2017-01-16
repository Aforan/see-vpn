from keyserv.settings import *

server_address = '35.167.237.255'
max_keys_per_user = 3

crt_dir = os.path.join(USER_PATH, 'keys/')
csr_dir = os.path.join(USER_PATH, 'keys/')
ccd_dir = os.path.join(USER_PATH, 'ccd/')
ca_path = os.path.join(USER_PATH, 'keys/ca.crt')
doc_dir = os.path.join(USER_PATH, 'doc/')
