from django import forms

import mistune
from captcha.fields import CaptchaField

from .models import Comment

class CommentForm(forms.ModelForm):
	nickname = forms.CharField(
		label = '昵称',
		max_length = 50,
		widget = forms.widgets.Input(
			attrs = {'class': 'form-control', 'style': "width: 60%;"}
			)
		)
	email = forms.CharField(
		label='Email',
		max_length = 50,
		widget = forms.widgets.EmailInput(
			attrs = {'class': 'form-control', 'style': "width: 60%;"}
			)

		)
	website = forms.CharField(
		label = '网站',
		max_length = 100,
		widget = forms.widgets.URLInput(
			attrs = {'class': 'form-control', 'style': "width:60%;"}

			)
		)
	content = forms.CharField(
		label = "内容",
		max_length = 500,
		widget = forms.widgets.Textarea(
			attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
			)
		)
	captcha = CaptchaField()
	def clean_content(self):
		content = self.cleaned_data.get('content')
		if len(content)<10:
			raise forms.ValidationError('请您继续锦上添花！')
		content = mistune.markdown(content)
		return content

	class Meta:
		model = Comment
		fields = ['nickname', 'email', 'website', 'content']