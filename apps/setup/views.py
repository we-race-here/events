from allauth.account.utils import perform_login
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from importlib import import_module


class DynamicFormView(View):
    template_name = 'dynamic_form.html'

    def get_form_class(self, form_type):
        module_path, form_name = form_type.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, form_name, None)

    def get_form_instance(self, form_type, data, request=None):
        form_initialization_map = {
            'users.forms.UserLoginForm': {'data': data, 'request': request},
            # Add other forms here as needed
        }

        default_initialization = {'data': data}

        return self.get_form_class(form_type)(**form_initialization_map.get(form_type, default_initialization))

    def post(self, request, *args, **kwargs):
        form_type = request.GET.get('type')
        form = self.get_form_instance(form_type, request.POST, request)

        if form.is_valid():
            if form_type == 'users.forms.UserLoginForm':
                user = form.user
                perform_login(request, user, email_verification="optional")
                return JsonResponse({"redirect": True, "url": "/home"})
            elif form_type == 'users.forms.UserSignupForm':
                user = form.save(request=request)
                print(user)
                perform_login(request, user, email_verification="optional")
                return JsonResponse(
                    {"status": True, "message": "Signup successful", "redirect": True, "url": "/home"})
            else:
                instance = form.save(request=request)
                return JsonResponse({"status": True, "message": "success"})
        else:
            return render(request, self.template_name, {'form': form, 'form_type': form_type})

    def get(self, request, *args, **kwargs):
        form_type = request.GET.get('type')
        form_class = self.get_form_class(form_type)

        if form_class:
            return render(request, self.template_name, {'form': form_class(), 'form_type': form_type})
        else:
            return render(request, 'error.html', {'error': 'Invalid form type', 'form_type': form_type})
