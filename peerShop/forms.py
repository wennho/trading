from django import forms


class SignupForm(forms.Form):
    terms_conditions = forms.BooleanField(required=True,
                                          error_messages={'required': 'Acceptance required'})

    def signup(self, request, user):
        user.save()