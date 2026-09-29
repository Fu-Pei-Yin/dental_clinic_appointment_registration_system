from django import forms
from patient.models import Register
from basic.models import Info
from captcha.fields import CaptchaField
class RegisterForm(forms.ModelForm):
	class Meta:
		model=Register
		fields=['patient_name','dentist','service','appointment_date']
	def __init__(self,*args,**kwargs):
		super(RegisterForm,self).__init__(*args,**kwargs)
		self.fields['patient_name'].label='名字'
		self.fields['dentist'].label='醫師'
		self.fields['service'].label='治療項目'
		self.fields['appointment_date'].label='預約日期'
		self.fields['appointment_date'].widget=forms.DateInput(attrs={'class':'form-control','type':'date','required':True})
class InfoForm(forms.ModelForm):
	captcha=CaptchaField()
	class Meta:
		model=Info
		fields=['user_name','user_ID','user_secret','user_address','user_tel','user_birth','user_identity']
	def __init__(self,*args,**kwargs):
		super(InfoForm,self).__init__(*args,**kwargs)
		self.fields['user_name'].label='姓名'
		self.fields['user_ID'].label='身份證字號'
		self.fields['user_ID'].widget.attrs['readonly']=True
		self.fields['user_ID'].widget.attrs['class']='disabled-field'
		self.fields['user_secret'].label='密碼'
		self.fields['user_secret'].widget=forms.PasswordInput()
		self.fields['user_address'].label='住址'
		self.fields['user_tel'].label='電話'
		self.fields['user_birth'].label='生日'
		self.fields['user_birth'].widget.attrs['readonly']=True
		self.fields['user_birth'].widget.attrs['class']='disabled-field'
		self.fields['user_identity'].label='身份'
		self.fields['captcha'].label='不是機器人'
