from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=100)


class PersonalInfoForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    street = forms.CharField(max_length=200)
    psc = forms.CharField(max_length=10)
    municipality = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
