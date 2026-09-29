from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.forms import HiddenInput
from django.db.models import Q
from django.db import connections
import datetime
from basic.models import Info
from .models import Register
from basic.models import Service,Dentist
from .forms import InfoForm,RegisterForm
# Create your views here.
def info(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        patient=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if patient.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/patient_manage/')
    if request.method=="POST":
        info_form=InfoForm(request.POST,instance=patient)
        if info_form.is_valid():
            user_name=request.POST['user_name']
            user_ID=request.POST['user_ID']
            user_tel=request.POST['user_tel']
            user_address=request.POST['user_address']
            user_birth=request.POST['user_birth']
            user_identity=request.POST['user_identity']
            if len(user_name)<2 or len(user_name)>15:
                messages.add_message(request,messages.INFO,'使用者名稱須在2到15字之間')
                return HttpResponseRedirect(f'/info/')
            elif not(user_tel.isdigit() and len(user_tel)==10):
                messages.add_message(request,messages.INFO,'電話號碼需為10碼數字')
                return HttpResponseRedirect(f'/info/')
            elif user_identity not in ['normal','veterans','disability']:
                messages.add_message(request,messages.INFO,'身分別錯誤')
                return HttpResponseRedirect(f'/info/')
            else:
                info_form.save()
                messages.add_message(request,messages.SUCCESS,"病患資料已更新")
                return HttpResponseRedirect('/patient_manage/')
    else:
        info_form=InfoForm(instance=patient)
    return render(request,'patient/info.html',locals())
def register(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        patient=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if patient.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/patient_manage/')
    patients=Info.objects.all()
    dentists=Dentist.objects.all()
    services=Service.objects.all()
    patient_name=request.session['user_name'].strip()
    if request.method == "POST":
        register_form=RegisterForm(request.POST)
        register_form.fields['patient_name'].widget=HiddenInput()
        if register_form.is_valid():
            dentist_id=request.POST['dentist']
            service_id=request.POST['service']
            appointment_date=request.POST['appointment_date']
            if appointment_date < datetime.date.today().strftime('%Y-%m-%d'):
                messages.add_message(request,messages.WARNING,"預約日期不可為過去日期")
                return HttpResponseRedirect('/register/')
            if Register.objects.filter(patient_name=patient_name,appointment_date=appointment_date).exists():
                messages.add_message(request,messages.WARNING,f"「{patient_name}」在「{appointment_date}」已有預約記錄，不可重複預約")
                return HttpResponseRedirect('/search/')
            try:
                dentist=Dentist.objects.get(id=dentist_id)
                service=Service.objects.get(id=service_id)
            except (Dentist.DoesNotExist,Service.DoesNotExist):
                messages.add_message(request,messages.WARNING,"選擇的醫師或治療項目不存在")
                return HttpResponseRedirect('/register/')
            if service not in dentist.services.all():
                messages.add_message(request,messages.WARNING,f"醫師「{dentist.name}」未提供「{service.name}」服務")
                return HttpResponseRedirect('/register/')
            weekday_map={
                0: '星期一',1: '星期二',2: '星期三',3: '星期四',4: '星期五',5: '星期六',6: '星期日'}
            weekday_str=weekday_map[datetime.datetime.strptime(appointment_date,'%Y-%m-%d').weekday()]
            if not dentist.time.filter(time=weekday_str).exists():
                messages.add_message(request,messages.WARNING,f"醫師「{dentist.name}」在「{weekday_str}」未出診")
                return HttpResponseRedirect('/register/')
            new_register=register_form.save(commit=False)
            new_register.patient_name=patient_name
            new_register.save(using='default')
            messages.add_message(request,messages.SUCCESS,"掛號成功！我們會盡快與您聯絡確認")
            return HttpResponseRedirect('/search/')
    else:
        register_form=RegisterForm(initial={'patient_name': patient_name})
        register_form.fields['patient_name'].widget=HiddenInput()
    return render(request,'patient/register.html',locals())
def search(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        patient=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if patient.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/patient_manage/')
    query=request.GET.get('query','').strip()
    registers=Register.objects.all()
    user=request.session['user_name']
    today=datetime.date.today()
    if query:
        registers=registers.filter(Q(patient_name__icontains=query)|
                                    Q(dentist__name__icontains=query)|
                                    Q(service__name__icontains=query)|
                                    Q(appointment_date__icontains=query))
    else:
        registers=Register.objects.filter(patient_name=user).order_by('appointment_date')
    return render(request,'patient/search.html',locals())