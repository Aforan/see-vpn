server_address = 'ec2-35-165-123-143.us-west-2.compute.amazonaws.com'
is_server = False
is_vm = True
max_keys_per_user = 3

if is_server:
	crt_dir = '/home/ubuntu/keys/'
	csr_dir = '/home/ubuntu/keys/'
	ccd_dir = '/home/ubuntu/ccd/'

	ca_path = '/home/ubuntu/key/ca.crt'
elif is_vm:
	crt_dir = '/home/cad/keyserv/keys/'
	csr_dir = '/home/cad/keyserv/keys/'
	ccd_dir = '/home/cad/keyserv/ccd/'

	ca_path = '/home/cad/keyserv/keys/ca.crt'	
else:
	crt_dir = '/home/cad/Dropbox/SeniorDesign/KeyServ/keys/'
	csr_dir = '/home/cad/Dropbox/SeniorDesign/KeyServ/keys/'
	ccd_dir = '/home/cad/Dropbox/SeniorDesign/KeyServ/ccd/'

	ca_path = '/home/cad/Dropbox/SeniorDesign/KeyServ/keys/ca.crt'

