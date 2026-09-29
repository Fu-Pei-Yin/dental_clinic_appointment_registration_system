from django import forms
from basic.models import Service,Dentist,Info
class ServiceForm(forms.ModelForm):
	class Meta:
		model=Service
		fields=['name','description','price']
	def __init__(self,*args,**kwargs):
		super(ServiceForm,self).__init__(*args,**kwargs)
		self.fields['name'].label='治療項目'
		self.fields['description'].label='治療項目描述'
		self.fields['price'].label='治療價格'
class DentistForm(forms.ModelForm):
	class Meta:
		model=Dentist
		fields=['name','services','time']
	def __init__(self,*args,**kwargs):
		super(DentistForm,self).__init__(*args,**kwargs)
		self.fields['name'].label='醫師名字'
		self.fields['services'].label='治療項目'
		self.fields['time'].label='看診時間'
class PatientForm(forms.ModelForm):
	class Meta:
		model=Info
		fields=['user_name','user_address','user_tel','can_manage','user_identity']
	def __init__(self,*args,**kwargs):
		super(PatientForm,self).__init__(*args,**kwargs)
		self.fields['user_name'].label='姓名'
		self.fields['user_address'].label='住址'
		self.fields['user_tel'].label='電話'
		self.fields['can_manage'].label='管理者'
		self.fields['user_identity'].label='身份'