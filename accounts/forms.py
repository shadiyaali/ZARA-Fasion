from django import forms
from .models import Account,UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
       'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class' : 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': ' First Name','class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class' : 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email','class' : 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number','class' : 'form-control'}),
        }
 
     
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')  
        confirm_password = cleaned_data.get('confirm_password')   

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )  


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': ' First Name','class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class' : 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number','class' : 'form-control'}),
                
        }
    
class UserprofileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid':("image files only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self, *args, **kwargs):
      super(UserprofileForm,self).__init__(*args,**kwargs)  
      for field in self.fields:
          self.fields[field].widget.attrs['class'] = 'form-control' 