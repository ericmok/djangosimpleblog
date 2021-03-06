from django import forms

from users.models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')

        if password1 != password2:
            raise forms.ValidationError('The two password fields need to match.')

        return password2

    def save(self):
        user = super(RegisterForm, self).save()
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email')