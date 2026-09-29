from django import forms
from . import models
from basic.models import Info
from captcha.fields import CaptchaField
class LoginForm(forms.Form):
	user_name=forms.CharField(label='請輸入名字',max_length=20)
	user_secret=forms.CharField(label='請輸入密碼',max_length=20,widget=forms.PasswordInput())
	captcha=CaptchaField(label='你不是機器人')
class PasswordForm(forms.ModelForm):
	captcha=CaptchaField()
	class Meta:
		model=Info
		fields=['user_ID']
	def __init__(self,*args,**kwargs):
		super(PasswordForm,self).__init__(*args,**kwargs)
		self.fields['user_ID'].label='身份證字號'
		self.fields['captcha'].label='不是機器人'
class LogonForm(forms.ModelForm):
	captcha=CaptchaField()
	class Meta:
		model=models.Info
		fields=['user_name','user_ID','user_secret','user_address','user_tel','user_birth','user_identity']
	def __init__(self,*args,**kwargs):
		super(LogonForm,self).__init__(*args,**kwargs)
		self.fields['user_name'].label='請輸入名字'
		self.fields['user_ID'].label='請輸入身份證字號'
		self.fields['user_secret'].label='請輸入密碼'
		self.fields['user_secret'].widget=forms.PasswordInput()
		self.fields['user_address'].label='請輸入住址'
		self.fields['user_tel'].label='請輸入電話'
		self.fields['user_birth'].label='出生日期'
		self.fields['user_birth'].widget=forms.DateInput(attrs={'class':'form-control','type':'date','required':True})
		self.fields['user_identity'].label='請選擇身份'
		choices=[('normal','一般身份'),('veterans','退伍軍人'),('disability','領有殘障手冊')]
		self.fields['user_identity'].choices=choices
		self.fields['captcha'].label='不是機器人'
