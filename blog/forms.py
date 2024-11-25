from django import forms
from landing.models import Contact, Newsletter


# blog/forms.py
# class ContactUsForm(forms.Form):
#     name = forms.CharField(
#         max_length=100, widget=forms.TextInput(attrs={"class": "form-input"})
#     )
#     email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-input"}))
#     message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-textarea"}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "subject": forms.TextInput(attrs={"class": "form-input"}),
            "message": forms.Textarea(attrs={"class": "form-textarea"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].required = False


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-input"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
