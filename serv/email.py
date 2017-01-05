from django.utils import timezone
from django.core.mail import send_mail


def send_user_request_notification(user_details):
	msg = \
	"""
New User Request:

Username:\t{username}
Organization:\t{org_name}
Contact:\t\t{contact_name}\t|\t{contact_email}\t|\t{contact_phone}

Requested at: {datetime}
	""".format(username=user_details.user.username,
			   org_name=user_details.org_name,
			   contact_name=user_details.contact_name,
			   contact_email=user_details.contact_email,
			   contact_phone=(user_details.contact_phone 
			   		if user_details.contact_phone is not None else ""),
			   datetime=timezone.now())

	send_mail('New User Request from: {}'.format(user_details.user.username),
			  msg, 'notification@see-vpn.com', ['Andrew.Foran.VR@gmail.com'],
			  fail_silently=False)

def send_user_activation_notification(user_details):
	msg = \
	"""
Your VPN account has been activated, you are now able to log in and download 
your VPN configuration files and instructions.

Contact the admin for any questions
	"""

	send_mail('SEE VPN Account activated', msg, 'notifications@see-vpn.com', 
			  [user_details.user.email], fail_silently=False)
