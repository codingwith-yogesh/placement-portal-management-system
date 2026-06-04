from django import forms
from django.contrib.auth.models import User
from .models import Job, Student, Company, Application


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
        

class CompanyRegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password'
        ]
        

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'package',
            'minimum_cgpa',
            'deadline'
        ]

        widgets = {
            'deadline': forms.DateInput(
                attrs={'type': 'date'}
            )
        }
        
        
class ResumeForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = ['resume']
        
        
class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'phone',
            'cgpa',
            'branch',
            'passing_year'
        ]