import os
import django
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from serv import settings

##################################################
#   Initialize Django before importing any models!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keyserv.settings')
django.setup()

if not django_settings.configured:
    django_settings.configure()

##################################################

from serv.models import KeyModel, UserDetailsModel

##################################################
#	Key Stuff

class OutOfKeysException(Exception): pass
class InvalidKeyException(Exception): pass
class NonExistingKeyException(Exception): pass

def get_first_unassigned_key():
	qs = KeyModel.objects.filter(userdetailsmodel__isnull=True)
	return qs.first()

def assign_first_available_key_to_user(user_details):
	key = get_first_unassigned_key()
	if key == None:
		raise OutOfKeysException("Can't assign a key")
	
	if user_details is not None:
		user_details.key = key
		user_details.save()

def get_assigned_keys():
	return KeyModel.objects.filter(userdetailsmodel__isnull=False).all()

def has_key(name):
	qs = KeyModel.objects.filter(name=name)
	return qs.exists()

def get_key(name):
	qs = KeyModel.objects.filter(name=name)
	return qs.first()

def create_key(name):
	if has_key(name):
		raise ExistingKeyException("Attempt to create an existing key")

	key = KeyModel(name=name)
	valid, error = validate_key_model(key)

	if valid:
		key.save()
	else:
		raise InvalidKeyException(error)

def delete_key(name):
	key = get_key(name)

	if key != None:
		key.delete()
	else:
		raise NonExistingKeyException("Cannot delete a non-existing key")

def validate_key_model(key):
	crt_check = os.path.isfile(key.crt_path)
	key_check = os.path.isfile(key.key_path)
	ccd_check = os.path.isfile(key.ccd_path)

	return ((crt_check and key_check and ccd_check), 
			"crt_check={} key_check={} ccd_check={}"\
			.format(crt_check, key_check, ccd_check))

def assign_key(key_name, user):
	if get_assigned_key_count_for_user(user) >= settings.max_keys_per_user:
		raise TooManyKeysForUserException()

	key = get_key(key_name)

	if key == None:
		raise NonExistingKeyException("Can't assign a key to {}".format(user.username))

	key.user = user
	key.save()

def unassign_key(key_name):
	key = get_key(key_name)

	if key == None:
		raise NonExistingKeyException("Can't unassign a key to {}".format(user.username))

	key.user = None
	key.save()

##################################################
#	User Details Stuff

class InvalidUserDetailsArgumentException(Exception): pass
class ExistingUserDetailsException(Exception): pass
class NonExistingUserDetailsException(Exception): pass

def get_user_details(username):
	qs = UserDetailsModel.objects.filter(user__username=username)
	return qs.first()


def get_user_details_from_user(user):
	details = user.userdetailsmodel_set.first()
	return details

def has_user_details(username):
	qs = UserDetailsModel.objects.filter(user__username=username)	
	return qs.exists()

def get_all_user_details():
	qs = UserDetailsModel.objects.all()
	return qs

def create_user_details(username=None, password=None, is_active=True,
						org_name=None, contact_name=None, contact_email=None,
						contact_phone=None):

	if username is None: 
		raise InvalidUserDetailsArgumentException('Must provide a username to create details')

	if password is None: 
		raise InvalidUserDetailsArgumentException('Must provide a password to create details')

	if org_name is None: 
		raise InvalidUserDetailsArgumentException('Must provide a org_name to create details')

	if contact_name is None: 
		raise InvalidUserDetailsArgumentException('Must provide a contact_name to create details')

	if contact_email is None: 
		raise InvalidUserDetailsArgumentException('Must provide a contact_email to create details')

	if has_user_details(username):
		raise ExistingUserDetailsException('This user already has details')

	user = User.objects.create_user(username, contact_email, password)
	user.is_active = is_active

	user.save()

	user = User.objects.get(username=username)
	details = UserDetailsModel(user=user, org_name=org_name, contact_name=contact_name, 
							   contact_email=contact_email, contact_phone=contact_phone)

	details.save()

def delete_user_details(username):
	details = get_user_details(username)

	if details is None:
		raise NonExistingUserDetailsException('Cannot delete a nonexisting user details')

	details.delete()
