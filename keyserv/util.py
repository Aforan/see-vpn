import traceback
from django.shortcuts import render

##########################################################################
########                   View Helper Functions                  ########
##########################################################################

def base_view(view):
    def b(request, *args, **kwargs):
        _data = { 'user' : request.user, 
        		  'is_admin' : (request.user.has_perm('serv.admin_users') 
        		  			    if request.user else False) }

        response = view(request, *args, _data=_data, **kwargs)
        return response

    return b