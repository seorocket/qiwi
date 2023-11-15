from django import forms

class TaskForm(forms.Form):
    qiwi_wallet = forms.CharField(max_length=20)
    qiwi_pass = forms.CharField(max_length=50, widget=forms.PasswordInput)
    phones = forms.CharField(widget=forms.Textarea)
    amount = forms.IntegerField()
