from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
	username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label="密码", max_length=256, widget = forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.Form):
    
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
'''class DownloadForm(forms.Form):

	url = forms.CharField(label="下载")'''
class UpdateForm(forms.Form):

	username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
	new_password = forms.CharField(label="新密码",max_length=256, widget= forms.PasswordInput(attrs={'class': 'form-control'}))
	re_password = forms.CharField(label="确认密码",max_length=256, widget= forms.PasswordInput(attrs= {'class': 'form-control'}))
	email = forms.EmailField(label="已注册邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
