from django import forms

class bestClickerForm(forms.Form):
    dll_name = forms.CharField(label="DLL name", max_length=20)
    exe_name = forms.CharField(label="EXE name", max_length=20)