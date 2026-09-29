from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.db.models import Q
import datetime
from .forms import LoginForm,LogonForm,PasswordForm
from .models import Info
from .models import Service,Dentist,Contact
# Create your views here.
def index(request):
	services=Service.objects.all()
	if 'user_name' in request.session:
		user_name=request.session['user_name']
	if request.session.test_cookie_worked():
		request.session.delete_test_cookie()
		messages.add_message(request,messages.SUCCESS,'cookie supported')
	else:
		messages.add_message(request,messages.WARNING,'cookie not supported')
	request.session.set_test_cookie()
	return render(request,'basic/index.html',locals())
def login(request):
	if request.method=="POST":
		login_form=LoginForm(request.POST)
		if login_form.is_valid():
			user_name=request.POST['user_name']
			user_secret=request.POST['user_secret']
			try:
				user=Info.objects.get(user_name=user_name)
				if user_secret==user.user_secret:
					request.session['user_name']=user.user_name
					request.session['user_ID']=user.user_ID
					request.session['user_tel']=user.user_tel
					request.session['user_birth']=user.user_birth.strftime('%Y-%m-%d')
					request.session['can_manage']=user.can_manage
					request.session['user_identity']=user.user_identity
					messages.add_message(request,messages.SUCCESS,f"歡迎 {user.user_name} 登入！")
					if user.can_manage==True:
						request.session['is_patient']=False
						request.session['is_manager']=True
					else:
						request.session['is_patient']=True
						request.session['is_manager']=False
					return HttpResponseRedirect('/')
				else:
					messages.add_message(request,messages.WARNING,'密碼輸入錯誤')
			except:
				messages.add_message(request,messages.WARNING,'找不到使用者')
		else:
			messages.add_message(request,messages.INFO,'輸入錯誤')
	else:
		login_form=LoginForm()
	return render(request,'basic/login.html',locals())
def logon(request):
	if request.method=='POST':
		logon_form=LogonForm(request.POST)
		if logon_form.is_valid():
			user_name=request.POST['user_name']
			user_secret=request.POST['user_secret']
			user_ID=request.POST['user_ID']
			user_address=request.POST['user_address']
			user_tel=request.POST['user_tel']
			user_birth=request.POST['user_birth']
			user_identity=request.POST['user_identity']
			if  Info.objects.filter(user_ID=user_ID).exists():
				messages.add_message(request,messages.WARNING,'您已註冊')
			elif len(user_name)<2 or len(user_name)>15:
				messages.add_message(request,messages.INFO,'使用者名稱須在2到15字之間')
			elif len(user_secret)<6:
				messages.add_message(request,messages.INFO,'密碼長度至少6字元')
			elif user_secret.isdigit() or user_secret.isalpha():
				messages.add_message(request,messages.INFO,'密碼不能只包含數字或字母')
			elif not(len(user_ID)==10 and user_ID[0].isalpha() and user_ID[1:].isdigit()):
				messages.add_message(request,messages.INFO,'請輸入有效的身分證字號（1 英文 + 9 數字）')
			elif not(user_tel.isdigit() and len(user_tel)==10):
				messages.add_message(request,messages.INFO,'電話號碼需為10碼數字')
			else:
				try:
					birth_date=datetime.datetime.strptime(user_birth,"%Y-%m-%d").date()
				except ValueError:
					messages.add_message(request,messages.INFO,'生日格式錯誤，請使用 YYYY-MM-DD 格式')
					return render(request,'patient/logon.html',locals())
				if birth_date > datetime.date.today():
					messages.add_message(request,messages.INFO,'生日日期不可為未來日期')
					return render(request,'patient/logon.html',locals())
				if user_identity not in ['normal','veterans','disability']:
					messages.add_message(request,messages.INFO,'身分別錯誤')
				else:
					logon_form.save()
					messages.add_message(request,messages.SUCCESS,'註冊成功')
					return HttpResponseRedirect('/login/')
		else:
			messages.add_message(request,messages.WARNING,'所有欄位皆必填')
	else:
		logon_form=LogonForm()
	return render(request,'basic/logon.html',locals())
def password_recovery(request):
    if request.method == "POST":
        password_form=PasswordForm(request.POST)
        if password_form.is_valid():
            user_ID=request.POST['user_ID']
            try:
                user=Info.objects.get(user_ID=user_ID)
                messages.add_message(request,messages.SUCCESS,f"您的密碼是：{user.user_secret}")
                return HttpResponseRedirect('/login/')
            except:
                messages.add_message(request,messages.WARNING,"找不到該身分證字號的用戶")
        else:
            messages.add_message(request,messages.WARNING,"請填寫完整資訊")
    else:
        password_form=PasswordForm()
    return render(request,'basic/password_recovery.html',locals())
def logout(request):
	if 'user_name' in request.session:
		Session.objects.all().delete()
		messages.add_message(request,messages.SUCCESS,"已登出")
	else:
		messages.add_message(request,messages.INFO,"尚未登入")
	return HttpResponseRedirect('/')
def services(request):
	services=Service.objects.all()
	return render(request,'basic/services.html',locals())
def dentists(request):
	dentists=Dentist.objects.all()
	query=request.GET.get('query','').strip()
	if query:
		dentists=dentists.filter(Q(name__icontains=query)|
								Q(time__time__icontains=query)|
								Q(services__name__icontains=query)).distinct()
		print(dentists)
	return render(request,'basic/dentists.html',locals())
def contact(request):
	if request.method=="POST":
		name=request.POST['name'].strip()
		email=request.POST['email']
		message=request.POST['message']
		if len(name)<2or len(name)>15:
			messages.add_message(request,messages.INFO,'使用者名稱須在2到15字之間')
			return HttpResponseRedirect('/contact/')
		contact=Contact.objects.create(name=name,email=email,message=message)
		contact.save()
		messages.add_message(request,messages.SUCCESS,"您的訊息已成功送出，我們會盡快與您聯絡")
	return render(request,'basic/contact.html')
