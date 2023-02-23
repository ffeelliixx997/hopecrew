from django import forms
from chat.models import Contact


class ContactForm(forms.ModelForm):
    model = Contact
    fields = "__all__"

# class ProfileForm(forms.ModelForm):
#     model = Profile
#     fields = "__all__"
