from serv import settings
from serv import service

def ip_from_suffix(suffix):
	return '{}.{}'.format(settings.base_ip, suffix)

def client_file(client_name, ip_suffix):
	assert ip_suffix < 255, 'Cannot use an IP Suffix >= 255'
	assert ip_suffix > 0,   'Cannot use an IP Suffix <= 0'

	with open(settings.ccd_dir + client_name, 'w') as f:
		f.write('ifconfig-push {} {}'\
			.format(ip_from_suffix(ip_suffix),
				ip_from_suffix(ip_suffix+1)))

def auto_create_keys():
	import os
	keys = os.listdir(settings.ccd_dir)

	for key in keys:
		try:
			service.create_key(key)
		except Exception as e:
			print('Could not create key {} got an exception'.format(key))
			print(e)
