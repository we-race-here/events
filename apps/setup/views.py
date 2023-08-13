from django.shortcuts import render
from django.views import View
from importlib import import_module


class DynamicFormView(View):
    template_name = 'dynamic_form.html'

    def get_form_class(self, app_name, form_name):
        module = import_module(f"apps.{app_name}.forms")
        return getattr(module, form_name, None)

    def get(self, request, *args, **kwargs):
        form_type = request.GET.get('type')  # e.g., 'event.EventOrgAdminForm'
        app_name, form_name = form_type.split('.')
        form_class = self.get_form_class(app_name, form_name)

        if form_class:
            return render(request, self.template_name, {'form': form_class(),'form_type' : form_type})
        else:
            return render(request, 'error.html', {'error': 'Invalid form type', 'form_type' : form_type})

    def post(self, request, *args, **kwargs):
        form_type = request.GET.get('type')
        app_name, form_name = form_type.split('.')
        form_class = self.get_form_class(app_name, form_name)

        form = form_class(request.POST)
        if form.is_valid():
            # Handle successful form submission
            return render(request,self.template_name)
        else:
            # Return form with validation errors
            return render(request, self.template_name, {'form': form, 'form_type' : form_type})
