from django.forms import RadioSelect

class BootstrapDateTimePickerInput(RadioSelect):
    template_name = 'widgets/bootstrap_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        print(attrs)
        attrs['name'] = 'hello'
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        context['widget']['label'] = 'Mylabel'
        return context


# from django import forms


# class ToggleWidget(forms.widgets.CheckboxInput):
#     class Media:
#         css = {'all': (
#             "https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css", )}
#         js = ("https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js",)

#     def __init__(self, attrs=None, *args, **kwargs):
#         attrs = attrs or {}

#         default_options = {
#             'toggle': 'toggle',
#             'offstyle': 'danger'
#         }
#         options = kwargs.get('options', {})
#         default_options.update(options)
#         for key, val in default_options.items():
#             attrs['data-' + key] = val

#         super().__init__(attrs)