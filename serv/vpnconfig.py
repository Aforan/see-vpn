_READMETEXT = """
VPN Configuration Instructions:
Written By: Andrew Foran
Contact: andrew.foran.vr@gmail.com

Contents:
	-	README				This File
	-	doc					Directory containing documentation, **start there**
		-	SEE VPN Installation and Configuration
		-	Pitch SEE VPN Configuration
		-	MAK SEE VPN Configuration
	-	Windows				Directory containing Windows specific config and scripts
		-	runvpn.bat			Bat to run the VPN client
		-	vpninfo.bat			Bat to return the ip address of your vpn adapter
		-	client.ovpn			OpenVPN Client configuration file, see Config
	-	OSX					Directory containing Mac OS X specific config
		-	client.ovpn			OpenVPN Client configuration file, see Config

	-	Keys (In both Windows and OSX directories)
		-	ca.crt			Certificate Authority Key
		-	client.crt		Client certificate, Unique to YOU
		-	client.key		Client key, This should be kept secret, don't give away

Usage: 
-	Double click the "runvpn.bat" file
-	A terminal window should open and dump logs for it's initialization
-	You should see "Initialization Sequence Completed" when complete

Notes:
vpninfo.bat will not tell you if the vpn is running, it simply returns the last ip address
			used by your openvpn network adapter.  Make sure the vpn is running by checking
			the output of runvpn.bat.  Alternatively, you can locate the ip address of your
			vpn client by running ipconfig and looking for it.  You can use 
			$ openvpn --show-adapters to show which adapter is used by openvpn

"""

_RUNVPNTEXT = """::Hacky hacks from here: http://stackoverflow.com/questions/11525056/how-to-create-a-batch-file-to-run-cmd-as-administrator

@echo off
:: BatchGotAdmin
::-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
::--------------------------------------

openvpn --config "client.ovpn"

"""


_VPNINFOBAT = """::Attempt to extract the ip address of the adapter connected to the VPN
::This will return the last ip address used to connect if the vpn is not connected
::This script WILL NOT tell you if the vpn is connected or not, see the runvpn output for connection status

@echo off
for /f "delims=" %%i in ('openvpn --show-adapters') do set _test=%%i
echo Adapter: %_test%
SET _endbit=%_test:*' {=%
CALL SET _result=%%_test:%_endbit%=%%
SET _result=%_result:' {=%
SET _result=%_result:'=%

echo Extracted Adapter Name: %_result% 

for /f "delims=" %%i in ('netsh interface ip show addresses "%_result%"') do echo %%i

pause
"""

_WINCLIENTCONFIGTEXT = """
##############################################
# Sample client-side OpenVPN 2.0 config file #
# for connecting to multi-client server.     #
#                                            #
# This configuration can be used by multiple #
# clients, however each client should have   #
# its own cert and key files.                #
#                                            #
# On Windows, you might want to rename this  #
# file so it has a .ovpn extension           #
##############################################

# Specify that we are a client and that we
# will be pulling certain config file directives
# from the server.
client

# Use the same setting as you are using on
# the server.
# On most systems, the VPN will not function
# unless you partially or fully disable
# the firewall for the TUN/TAP interface.
;dev tap
dev tun

# Windows needs the TAP-Windows adapter name
# from the Network Connections panel
# if you have more than one.  On XP SP2,
# you may need to disable the firewall
# for the TAP adapter.
;dev-node "Ethernet 2"

# Are we connecting to a TCP or
# UDP server?  Use the same setting as
# on the server.
proto tcp
;proto udp

# The hostname/IP and port of the server.
# You can have multiple remote entries
# to load balance between the servers.
remote {remote_address}
port 443
;remote my-server-2 1194

# Choose a random host from the remote
# list for load-balancing.  Otherwise
# try hosts in the order specified.
;remote-random

# Keep trying indefinitely to resolve the
# host name of the OpenVPN server.  Very useful
# on machines which are not permanently connected
# to the internet such as laptops.
resolv-retry infinite

# Most clients don't need to bind to
# a specific local port number.
nobind

# Downgrade privileges after initialization (non-Windows only)
;user nobody
;group nobody

# Try to preserve some state across restarts.
persist-key
persist-tun

# If you are connecting through an
# HTTP proxy to reach the actual OpenVPN
# server, put the proxy server/IP and
# port number here.  See the man page
# if your proxy server requires
# authentication.
;http-proxy-retry # retry on connection failures
;http-proxy [proxy server] [proxy port #]

# Wireless networks often produce a lot
# of duplicate packets.  Set this flag
# to silence duplicate packet warnings.
;mute-replay-warnings

# SSL/TLS parms.
# See the server config file for more
# description.  It's best to use
# a separate .crt/.key file pair
# for each client.  A single ca
# file can be used for all clients.
ca "Keys\\\\ca.crt"
cert "Keys\\\\client.crt"
key "Keys\\\\client.key"

# Verify server certificate by checking
# that the certicate has the nsCertType
# field set to "server".  This is an
# important precaution to protect against
# a potential attack discussed here:
#  http://openvpn.net/howto.html#mitm
#
# To use this feature, you will need to generate
# your server certificates with the nsCertType
# field set to "server".  The build-key-server
# script in the easy-rsa folder will do this.
;ns-cert-type server

# If a tls-auth key is used on the server
# then every client must also have the key.
;tls-auth ta.key 1

# Select a cryptographic cipher.
# If the cipher option is used on the server
# then you must also specify it here.
;cipher x

# Enable compression on the VPN link.
# Don't enable this unless it is also
# enabled in the server config file.
comp-lzo

# Set log file verbosity.
verb 3

# Silence repeating messages
;mute 20
"""

_OSXCLIENTCONFIGTEXT = """
##############################################
# Sample client-side OpenVPN 2.0 config file #
# for connecting to multi-client server.     #
#                                            #
# This configuration can be used by multiple #
# clients, however each client should have   #
# its own cert and key files.                #
#                                            #
# On Windows, you might want to rename this  #
# file so it has a .ovpn extension           #
##############################################

# Specify that we are a client and that we
# will be pulling certain config file directives
# from the server.
client

# Use the same setting as you are using on
# the server.
# On most systems, the VPN will not function
# unless you partially or fully disable
# the firewall for the TUN/TAP interface.
;dev tap
dev tun

# Windows needs the TAP-Windows adapter name
# from the Network Connections panel
# if you have more than one.  On XP SP2,
# you may need to disable the firewall
# for the TAP adapter.
;dev-node "Ethernet 2"

# Are we connecting to a TCP or
# UDP server?  Use the same setting as
# on the server.
proto tcp
;proto udp

# The hostname/IP and port of the server.
# You can have multiple remote entries
# to load balance between the servers.
remote {remote_address}
port 443
;remote my-server-2 1194

# Choose a random host from the remote
# list for load-balancing.  Otherwise
# try hosts in the order specified.
;remote-random

# Keep trying indefinitely to resolve the
# host name of the OpenVPN server.  Very useful
# on machines which are not permanently connected
# to the internet such as laptops.
resolv-retry infinite

# Most clients don't need to bind to
# a specific local port number.
nobind

# Downgrade privileges after initialization (non-Windows only)
;user nobody
;group nobody

# Try to preserve some state across restarts.
persist-key
persist-tun

# If you are connecting through an
# HTTP proxy to reach the actual OpenVPN
# server, put the proxy server/IP and
# port number here.  See the man page
# if your proxy server requires
# authentication.
;http-proxy-retry # retry on connection failures
;http-proxy [proxy server] [proxy port #]

# Wireless networks often produce a lot
# of duplicate packets.  Set this flag
# to silence duplicate packet warnings.
;mute-replay-warnings

# SSL/TLS parms.
# See the server config file for more
# description.  It's best to use
# a separate .crt/.key file pair
# for each client.  A single ca
# file can be used for all clients.
ca "Keys//ca.crt"
cert "Keys//client.crt"
key "Keys//client.key"

# Verify server certificate by checking
# that the certicate has the nsCertType
# field set to "server".  This is an
# important precaution to protect against
# a potential attack discussed here:
#  http://openvpn.net/howto.html#mitm
#
# To use this feature, you will need to generate
# your server certificates with the nsCertType
# field set to "server".  The build-key-server
# script in the easy-rsa folder will do this.
;ns-cert-type server

# If a tls-auth key is used on the server
# then every client must also have the key.
;tls-auth ta.key 1

# Select a cryptographic cipher.
# If the cipher option is used on the server
# then you must also specify it here.
;cipher x

# Enable compression on the VPN link.
# Don't enable this unless it is also
# enabled in the server config file.
comp-lzo

# Set log file verbosity.
verb 3

# Silence repeating messages
;mute 20
"""


import os
import io
import zipfile
from serv import settings
from io import BytesIO

def get_readme():
	return _READMETEXT

def get_bat_file():
	return _RUNVPNTEXT

def get_vpninfo_file():
	return _VPNINFOBAT

def get_config_file(remote_address, ismac=False):
	txt = _OSXCLIENTCONFIGTEXT if ismac else _WINCLIENTCONFIGTEXT
	return txt.format(remote_address=remote_address)

def get_ca_file():
	with open(settings.ca_path, 'r') as f:
		ca_str = io.StringIO(f.read())

	return ca_str.read()

def get_crt_file(key):
	with open(key.crt_path, 'r') as f:
		crt_str = io.StringIO(f.read())

	return crt_str.read()

def get_key_file(key):
	with open(key.key_path, 'r') as f:
		key_str = io.StringIO(f.read())

	return key_str.read()

def write_windows_conf(zf, key, nobatch=False):
	subdir = "VPNConfig"
	windir = "Windows"

	if not nobatch:
		bat_path = os.path.join(subdir, windir, 'runvpn.bat')
		zf.writestr(bat_path, get_bat_file().replace('\n', '\r\n'))

		vpninfo_path = os.path.join(subdir, windir, 'vpninfo.bat')
		zf.writestr(vpninfo_path, get_vpninfo_file().replace('\n', '\r\n'))

	config_path = os.path.join(subdir, windir, 'client.ovpn')
	zf.writestr(config_path, get_config_file(settings.server_address).replace('\n', '\r\n'))

	ca_path = os.path.join(subdir, windir, 'Keys', 'ca.crt')
	zf.writestr(ca_path, get_ca_file())

	crt_path = os.path.join(subdir, windir, 'Keys', 'client.crt')
	zf.writestr(crt_path, get_crt_file(key))

	key_path = os.path.join(subdir, windir, 'Keys', 'client.key')
	zf.writestr(key_path, get_key_file(key))

def write_osx_conf(zf, key):
	subdir = "VPNConfig"
	windir = "OSX"

	config_path = os.path.join(subdir, windir, 'client.ovpn')
	zf.writestr(config_path, get_config_file(settings.server_address, ismac=True).replace('\n', '\r\n'))

	ca_path = os.path.join(subdir, windir, 'Keys', 'ca.crt')
	zf.writestr(ca_path, get_ca_file())

	crt_path = os.path.join(subdir, windir, 'Keys', 'client.crt')
	zf.writestr(crt_path, get_crt_file(key))

	key_path = os.path.join(subdir, windir, 'Keys', 'client.key')
	zf.writestr(key_path, get_key_file(key))

def write_doc_files(zf):
	subdir = "VPNConfig"
	docdir = "doc"
	
	if not os.path.isdir(settings.doc_dir):
		return
	
	files = [f for f in os.listdir(settings.doc_dir) if os.path.isfile(os.path.join(settings.doc_dir, f))]

	for file in files:
		f = open(os.path.join(settings.doc_dir, file), "rb")
		fpath = os.path.join(subdir, docdir, file)

		zf.writestr(fpath, f.read())

def get_config_zip(key, nobatch=False):
	subdir = "VPNConfig"

	out = io.BytesIO()
	zf = zipfile.ZipFile(out, 'w')

	readme_path = os.path.join(subdir, 'README')
	zf.writestr(readme_path, get_readme().replace('\n', '\r\n'))

	write_windows_conf(zf, key, nobatch=nobatch)
	write_osx_conf(zf, key)
	write_doc_files(zf)

	zf.close()

	out.seek(0)
	return out

