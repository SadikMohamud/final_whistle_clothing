from django import forms


class ContactForm(forms.Form):
	name = forms.CharField(max_length=120)
	email = forms.EmailField()
	subject = forms.CharField(max_length=140)
	message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))