from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin



class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == '1':
                if modulename == "account.AdminViews":
                    pass
                elif modulename == "account.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("home"))
            elif user.user_type == '2':
                if modulename == "account.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("home"))
        else:
            if request.path == reverse("login"):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))