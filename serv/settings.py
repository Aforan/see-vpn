from keyserv.settings import *

server_address = 'ec2-35-162-242-30.us-west-2.compute.amazonaws.com'
max_keys_per_user = 3

crt_dir = os.path.join(USER_PATH, 'keys/')
csr_dir = os.path.join(USER_PATH, 'keys/')
ccd_dir = os.path.join(USER_PATH, 'ccd/')
ca_path = os.path.join(USER_PATH, 'keys/ca.crt')
