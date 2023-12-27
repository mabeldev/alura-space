from django.shortcuts import redirect
from django.contrib import messages

def check_authentication(view_func, *args, **kwargs):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Usuário não autenticado')
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapped
