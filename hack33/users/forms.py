from django import forms
from django.utils.translation import ugettext_lazy as _


INPUTS = {
    'text': forms.TextInput,
    'pass': forms.PasswordInput,
    'hidden': forms.HiddenInput,
    'checkbox': forms.CheckboxInput
}


# w = widget
def w(input_type, value=None):
    element = INPUTS.get(input_type, None)

    if element is None:
        raise KeyError('{} not found as input type'.format(input_type))

    if value is None:
        return element()

    attrs = {'placeholder': value}
    return element(attrs=attrs)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label=_('Име'), widget=w('text', 'Име'))
    last_name = forms.CharField(label=_('Фамилия'), widget=w('text', 'Фамилия'))
    github_account = forms.CharField(label=_('Github'), widget=w('text', 'Github'))
    linkedin_account = forms.CharField(label=_('Linkedin'), widget=w('text', 'Linkedin'))
    mac = forms.CharField(label=_('MAC'), widget=w('text', 'MAC'))
    phone = forms.CharField(label=_('Телефонен номер'), widget=w('text', 'Телефонен номер'))
    # signature = forms.CharField(label=_('Linkedin'), widget=w('text', 'Linkedin'))
    skype = forms.CharField(label=_('Skype'), widget=w('text', 'Skype'))
