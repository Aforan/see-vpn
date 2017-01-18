from django.utils.encoding import escape_uri_path
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def download_link(keyname):
	url = "/download_config/{}".format(keyname)
	url = escape_uri_path(url)

	return mark_safe("<a href='{}'>Download</a>".format(url))

@register.filter
def nobatch_download_link(keyname):
	url = "/nobat_download_config/{}".format(keyname)
	url = escape_uri_path(url)

	return mark_safe("<a href='{}'>Download</a>".format(url))

@register.filter
def unassign_link(key, redirect=None):
	url = "/unassign_key/{}".format(key.name)
	url = (url if redirect == None 
			  else url + '/{}'.format(redirect))

	url = escape_uri_path(url)
	return mark_safe("<a href='{}'>Unassign Key</a>".format(url))

@register.filter
def assign_link(key, redirect=None):
	url = "/assign_key/{}".format(key.name)
	url = (url if redirect == None 
			  else url + '/{}'.format(redirect))

	url = escape_uri_path(url)
	return mark_safe("<a href='{}'>Assign Key</a>".format(url))
