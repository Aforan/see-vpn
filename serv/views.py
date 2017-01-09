from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from keyserv.util import base_view
from serv.forms import KeyRequestForm, LoginForm, UserRequestForm, ToggleActiveUserForm
from serv import service
from serv import vpnconfig
from serv import email

@base_view
def login_view(request, _data={}):
	data = _data

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			data['message'] = 'Invalid Login Form'
		else:
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				# Redirect to a success page.
				return redirect('/')
			else:
				data['message'] = 'Invalid Login Credentials'

	data['form'] = LoginForm()
	return render(request, 'login.html', data)

def logout_view(request):
	logout(request)
	return redirect('/')

@base_view
def home_view(request, _data):
	if not request.user.is_authenticated:
		return render(request, 'home.html')
	else:
		data = _data

		user_details = service.get_user_details_from_user(request.user)
		if user_details is not None:
			print(user_details.key)
			data['key'] = user_details.key

		return render(request, 'user_home.html', data)

@base_view
@login_required(login_url='/login/')
@user_passes_test(lambda user: user.has_perm('serv.access_all_keys'), login_url='/login/')
def key_list_view(request, _data={}):
	data = _data

	keys = service.get_assigned_keys()
	data.update({'keys' : keys})
	return render(request, 'key_list.html', data)

@login_required(login_url='/login/')
def download_config_view(request, key_name=None):
	if request.method == 'GET':	
		if key_name == None:
			raise Exception('Must provide a key name to download a key')

		key = service.get_key(key_name)
		if key == None:
			raise Exception('Invalid key name provided')

		if key.userdetailsmodel is None or key.userdetailsmodel.user is None:
			raise Exception('Cannot get config file, no key is assigned to this client')
		
		user = key.userdetailsmodel.user
		
		if user != request.user and not request.user.has_perm('serv.admin_users'):
			raise Exception('Cannot get config file, invalid user')

		zip_file = vpnconfig.get_config_zip(key)

		resp = HttpResponse(zip_file.getvalue(), content_type="application/x-zip-compressed")
		resp['Content-Disposition'] = 'attachment; filename={}'.format('VPNConfig.zip')

		return resp

@base_view
def user_request_success_view(request, _data={}):
	return render(request, 'user_request_success.html', _data)

@base_view
def user_request_view(request, _data={}):
	data = _data

	if request.method == 'POST':
		form = UserRequestForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['password'] \
			!= form.cleaned_data['password_repeat']:
				data['message'] = 'Passwords don\'t match'
				data['form'] = form
			elif service.get_user_details(form.cleaned_data['username']):
				data['message'] = 'Username taken'
				data['form'] = form
			else:
				service.create_user_details(
					username=form.cleaned_data['username'], 
					password=form.cleaned_data['password'], 
					org_name=form.cleaned_data['organization_name'], 
					contact_name=form.cleaned_data['contact_name'], 
					contact_email=form.cleaned_data['contact_email'], 
					is_active=False)

				try:
					user_details = service.get_user_details(
										   form.cleaned_data['username'])
					user_details.save()
					email.send_user_request_notification(user_details)
				except Exception as e:
					print(e)

				return redirect('/user_request_success')
		else:
			data['message'] = 'User request form is not valid'

	if 'form' not in data: 
		data['form'] = UserRequestForm()

	return render(request, 'user_request.html', data)

@base_view
@login_required(login_url='/login/')
@user_passes_test(lambda user: user.has_perm('serv.admin_users'), login_url='/login/')
def user_admin_view(request, _data={}):
	data = _data

	if request.method == 'POST':
		form =  ToggleActiveUserForm(request.POST)
		if form.is_valid():
			try:
				user_details = service.get_user_details(form.cleaned_data['username'])
				new_activation = not user_details.user.is_active
				
				if new_activation:
					key = service.get_first_unassigned_key()
					user_details.key = key
				else:
					user_details.key = None
			
				user_details.user.is_active = new_activation
				user_details.user.save()
				user_details.save()

				email.send_user_activation_notification(user_details)
			except Exception as e:
				data['message'] = 'Error toggling user activation: {}'.format(e)
		else:
			data['message'] = 'Invalid toggle form'

	user_details = service.get_all_user_details()
	data['user_details'] = [{'details' : u, 
							 'form' : ToggleActiveUserForm(
									{ 'username' : u.user.username })}
							
							for u in user_details]

	return render(request, 'user_admin.html', data)
