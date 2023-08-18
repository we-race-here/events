from django import forms

class GoogleMapsWidget(forms.TextInput):
    template_name = 'widget/google_maps_widget.html'

    class Media:
        js = ('js/google_maps.js',)

    def __init__(self, attrs=None):
        default_attrs = {'class': 'google-maps-widget'}
        if attrs:
            default_attrs.update(attrs)
        super(GoogleMapsWidget, self).__init__(default_attrs)
