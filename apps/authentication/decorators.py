from django.http import HttpResponseForbidden


def admin_required(view_controller):
  def wrapper(request, *args, **kwargs):
    if request.user.role.name != 'ADMINISTRADOR':
      return HttpResponseForbidden()
    return view_controller(request, *args, **kwargs)
  return wrapper