from serv import settings
from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from phonenumber_field.modelfields import PhoneNumberField

class KeyModel(models.Model):
	name = models.CharField(max_length=64, blank=False, unique=True)

	@property
	def crt_path(self):
		return "{}{}.crt".format(settings.crt_dir, self.name)
	
	@property
	def key_path(self):
		return "{}{}.key".format(settings.csr_dir, self.name)

	@property
	def ccd_path(self):
		return "{}{}".format(settings.ccd_dir, self.name)

class UserDetailsModel(models.Model):
	user = models.ForeignKey(User, blank=True, null=True, default=None)
	key = models.OneToOneField(KeyModel, blank=True, null=True, default=None)

	org_name = models.CharField(max_length=64, blank=False, null=False)
	contact_name = models.CharField(max_length=64, blank=False, null=False)
	contact_email = models.EmailField(blank=False, null=False)
	contact_phone = PhoneNumberField(blank=True, null=True)


############################################################################
#	Set up permissions on these models if needed, once each time this module
#	is loaded, this is a really unfortunate way to have to do this...

_permission_check = False

if not _permission_check:
	if not Permission.objects.filter(codename='access_all_keys').exists():
		content_type = ContentType.objects.get_for_model(KeyModel)
		permission = Permission(content_type=content_type,
								codename='access_all_keys', 
								name='Can View All Clients')
		permission.save()

	if not Permission.objects.filter(codename='admin_users').exists():
		content_type = ContentType.objects.get_for_model(UserDetailsModel)
		permission = Permission(content_type=content_type,
								codename='admin_users', 
								name='Can Can Access User Admin Pages')
		permission.save()

	_permission_check = True
