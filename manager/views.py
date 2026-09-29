from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.contrib import messages
import datetime
from django.db.models import Q
from .forms import ServiceForm,DentistForm,PatientForm
from patient.forms import RegisterForm
from basic.models import Service,Dentist,Schedule
from patient.models import Register
from basic.models import Info,Contact
def service_manage(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    services=Service.objects.all()
    if request.method=="POST":
        service_form=ServiceForm(request.POST)
        if service_form.is_valid():
            name=request.POST['name'].strip()
            description=request.POST['description'].strip()
            price=request.POST['price'].strip()
            if Service.objects.filter(name=name).exists():
                messages.add_message(request,messages.WARNING,'治療項目已存在')
                return HttpResponseRedirect('/service_manage/')
            elif len(name)<2 or len(name)>15:
                messages.add_message(request,messages.INFO,'項目名稱須在2到15字之間')
                return HttpResponseRedirect('/service_manage/')
            else:
                if price:
                    price=int(price)
                    try:
                        if price < 0:
                            messages.add_message(request,messages.WARNING,"價格需為非負數字")
                            return HttpResponseRedirect('/service_manage/')
                    except:
                        messages.add_message(request,messages.WARNING,"價格格式錯誤")
                        return HttpResponseRedirect('/service_manage/')
                else:
                    price=150
            service_form.save()
            messages.add_message(request,messages.SUCCESS,f"已成功新增治療項目「{name}」")
            return HttpResponseRedirect('/service_manage/')
        else:
            messages.add_message(request,messages.WARNING,'所有欄位皆必填')
    else:
        service_form=ServiceForm()
    return render(request,'manager/service_manage.html',locals())
def service_edit(request,service_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        service=Service.objects.get(id=service_id)
    except:
        raise Http404('治療項目不存在')
    if request.method=="POST":
        service_form=ServiceForm(request.POST,instance=service)
        if service_form.is_valid():
            name=request.POST['name'].strip()
            description=request.POST['description'].strip()
            price=request.POST['price'].strip()
            if Service.objects.filter(name=name).exclude(id=service.id).exists():
                messages.add_message(request,messages.WARNING,'治療項目已存在')
                return HttpResponseRedirect('/service_manage/')
            elif len(name)<2 or len(name)>15:
                messages.add_message(request,messages.INFO,'項目名稱須在2到15字之間')
                return HttpResponseRedirect('/service_manage/')
            else:
                if price:
                    price=int(price)
                    try:
                        if price < 0:
                            messages.add_message(request,messages.WARNING,"價格需為非負數字")
                            return HttpResponseRedirect('/service_manage/')
                    except:
                        messages.add_message(request,messages.WARNING,"價格格式錯誤")
                        return HttpResponseRedirect('/service_manage/')
                else:
                    price=150
            service_form.save()
            messages.add_message(request,messages.SUCCESS,f"治療項目「{name}」已更新")
            return HttpResponseRedirect('/service_manage/')
        else:
            messages.add_message(request,messages.WARNING,'所有欄位皆必填')
    else:
        service_form=ServiceForm(instance=service)
    return render(request,'manager/service_edit.html',locals())
def service_delete(request,service_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        service=Service.objects.get(id=service_id)
    except:
        raise Http404('找不到該治療項目')
    service.delete()
    messages.add_message(request,messages.SUCCESS,f"治療項目「{service.name}」已刪除")
    return HttpResponseRedirect('/service_manage/')
def dentist_manage(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    dentists=Dentist.objects.all()
    services=Service.objects.all()
    schedules=Schedule.objects.using('baisc').all()
    if request.method=="POST":
        dentist_form=DentistForm(request.POST)
        if dentist_form.is_valid():
            name=request.POST['name'].strip()
            services=request.POST.getlist('services')
            time=request.POST.getlist('time')
            if not name:
                messages.add_message(request,messages.WARNING,"請輸入醫師名稱")
                return HttpResponseRedirect('/dentist_manage/')
            elif Dentist.objects.filter(name=name).exists():
                messages.add_message(request,messages.WARNING,'醫師已存在')
                return HttpResponseRedirect('/dentist_manage/')
            dentist_form.save()
            messages.add_message(request,messages.SUCCESS,f"醫師「{name}」已新增並設定看診時間")
            return HttpResponseRedirect('/dentist_manage/')
    else:
        dentist_form=DentistForm()
    return render(request,'manager/dentist_manage.html',locals())
def dentist_edit(request,dentist_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        dentist=Dentist.objects.get(id=dentist_id)
    except:
        raise Http404('查無該醫師資料')
    services=Service.objects.all()
    schedules=Schedule.objects.using('baisc').all()
    if request.method=="POST":
        dentist_form=DentistForm(request.POST,instance=dentist)
        if dentist_form.is_valid():
            name=request.POST['name'].strip()
            services=request.POST.getlist('services')
            time=request.POST.getlist('time')
            if not name:
                messages.add_message(request,messages.WARNING,"請輸入醫師名稱")
                return HttpResponseRedirect('/dentist_manage/')
            elif Dentist.objects.filter(name=name).exclude(id=dentist.id).exists():
                messages.add_message(request,messages.WARNING,'醫師已存在')
                return HttpResponseRedirect('/dentist_manage/')
            dentist_form.save()
            messages.add_message(request,messages.SUCCESS,f"醫師「{name}」已新增並設定看診時間")
            return HttpResponseRedirect('/dentist_manage/')
    else:
        dentist_form=DentistForm(instance=dentist)
    return render(request,'manager/dentist_edit.html',locals())
def dentist_delete(request,dentist_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        dentist=Dentist.objects.get(id=dentist_id)
    except:
        raise Http404('查無該醫師資料')
    dentist.delete()
    messages.add_message(request,messages.SUCCESS,f"醫師「{dentist.name}」已刪除")
    return HttpResponseRedirect('/dentist_manage')
def register_manage(request):
    today=datetime.date.today()
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    registers=Register.objects.all().order_by('appointment_date')
    patients=Info.objects.all()
    dentists=Dentist.objects.all()
    services=Service.objects.all()
    query=request.GET.get('query','').strip()
    if query:
        registers=registers.filter(
            Q(patient_name__icontains=query)|
            Q(dentist__name__icontains=query)|
            Q(service__name__icontains=query)|
            Q(appointment_date__icontains=query)
        )
    if request.method=="POST":
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            patient_name=request.POST['patient_name'].strip()
            dentist_id=request.POST['dentist']
            service_id=request.POST['service']
            appointment_date=request.POST['appointment_date']
            if not all([patient_name,dentist_id,service_id,appointment_date]):
                messages.warning(request,"請填寫所有欄位")
                return HttpResponseRedirect('/register_manage/')
            elif not Info.objects.filter(user_name=patient_name).exists():
                messages.warning(request,f"輸入的病患名稱「{patient_name}」不存在")
                return HttpResponseRedirect('/register_manage/')
            elif appointment_date < datetime.date.today().strftime('%Y-%m-%d'):
                messages.add_message(request,messages.WARNING,f"預約日期「{appointment_date}」不可為過去日期。")
                return HttpResponseRedirect('/register_manage/')
            elif Register.objects.filter(patient_name=patient_name,appointment_date=appointment_date).exists():
                messages.add_message(request,messages.WARNING,f"「{patient_name}」在「{appointment_date}」已有預約記錄，不可重複預約")
                return HttpResponseRedirect('/register_manage/')
            try:
                dentist=Dentist.objects.get(id=dentist_id)
                service=Service.objects.get(id=service_id)
            except (Dentist.DoesNotExist,Service.DoesNotExist):
                messages.warning(request,"醫師或治療項目不存在")
                return HttpResponseRedirect('/register_manage/')
            if service not in dentist.services.all():
                messages.warning(request,f"醫師「{dentist.name}」未提供「{service.name}」服務")
                return HttpResponseRedirect('/register_manage/')
            weekday_map={
                0: '星期一',1: '星期二',2: '星期三',3: '星期四',4: '星期五',5: '星期六',6: '星期日'}
            weekday_str=weekday_map[datetime.datetime.strptime(appointment_date,'%Y-%m-%d').weekday()]
            if not dentist.time.filter(time=weekday_str).exists():
                messages.warning(request,f"醫師「{dentist.name}」在「{weekday_str}」未出診")
                return HttpResponseRedirect('/register_manage/')
            register = register_form.save(commit=False)
            register.save(using='default')
            messages.success(request,f"「{patient_name}」已成功新增預約時間「{appointment_date}」")
            return HttpResponseRedirect('/register_manage/')
    else:
        register_form=RegisterForm()
    return render(request,'manager/register_manage.html',locals())
def register_edit(request,register_id):
    if 'user_name' not in request.session:
        messages.warning(request,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.warning(request,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        register=Register.objects.get(id=register_id)
    except:
        raise Http404('查無該預約')
    dentists=Dentist.objects.all()
    services=Service.objects.all()
    if request.method=="POST":
        register_form=RegisterForm(request.POST,instance=register)
        if register_form.is_valid():
            patient_name=request.POST['patient_name'].strip()
            dentist_id=request.POST['dentist']
            service_id=request.POST['service']
            appointment_date=request.POST['appointment_date']
            if not Info.objects.filter(user_name=patient_name).exists():
                messages.warning(request,f"輸入的病患名稱「{patient_name}」不存在")
                return HttpResponseRedirect('/register_manage/')
            elif Register.objects.filter(patient_name=patient_name,appointment_date=appointment_date).exclude(id=register.id).exists():
                messages.error(request,f"「{patient_name}」在「{appointment_date}」已有預約記錄，不可重複預約")
                return HttpResponseRedirect('/register_manage/')
            try:
                dentist=Dentist.objects.get(id=dentist_id)
                service=Service.objects.get(id=service_id)
            except (Dentist.DoesNotExist,Service.DoesNotExist):
                messages.warning(request,"醫師或治療項目不存在")
                return HttpResponseRedirect('/register_manage/')
            if service not in dentist.services.all():
                messages.warning(request,f"醫師「{dentist.name}」未提供「{service.name}」服務")
                return HttpResponseRedirect('/register_manage/')
            weekday_map={
                0: '星期一',1: '星期二',2: '星期三',3: '星期四',4: '星期五',5: '星期六',6: '星期日'}
            weekday_str=weekday_map[datetime.datetime.strptime(appointment_date,'%Y-%m-%d').weekday()]
            if not dentist.time.filter(time=weekday_str).exists():
                messages.warning(request,f"醫師「{dentist.name}」在「{weekday_str}」未出診")
                return HttpResponseRedirect('/register_manage/')
            register_form.save()
            messages.success(request,f"「{patient_name}」已成功更新預約")
            return HttpResponseRedirect('/register_manage/')
    else:
        register_form=RegisterForm(instance=register)
    return render(request,'manager/register_edit.html',locals())
def register_delete(request,register_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        register=Register.objects.get(id=register_id)
    except:
        raise Http404('')
    register.delete()
    messages.add_message(request,messages.SUCCESS,"預約已刪除")
    return HttpResponseRedirect('/register_manage/')
def patient_manage(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    query=request.GET.get('query','').strip()
    patients=Info.objects.all()
    if query:
        patients=patients.filter(Q(user_name__icontains=query)|
                                Q(user_ID__icontains=query)|
                                Q(user_tel__icontains=query))
    return render(request,'manager/patient_manage.html',locals())
def patient_edit(request,patient_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        patient=Info.objects.get(id=patient_id)
    except:
        raise Http404('查無該資訊')
    if request.method=="POST":
        patient_form=PatientForm(request.POST,instance=patient)
        if patient_form.is_valid():
            user_name=request.POST['user_name']
            user_tel=request.POST['user_tel']
            user_address=request.POST['user_address']
            user_identity=request.POST['user_identity']
            if Info.objects.filter(user_ID=patient.user_ID).exclude(id=patient.id).exists():
                messages.add_message(request,messages.WARNING,'使用者已存在')
                return HttpResponseRedirect(f'/patient_edit/{patient.id}/')
            elif len(user_name)<2 or len(user_name)>15:
                messages.add_message(request,messages.INFO,'使用者名稱須在2到15字之間')
                return HttpResponseRedirect(f'/patient_edit/{patient.id}/')
            elif not(user_tel.isdigit() and len(user_tel)==10):
                messages.add_message(request,messages.INFO,'電話號碼需為10碼數字')
                return HttpResponseRedirect(f'/patient_edit/{patient.id}/')
            elif user_identity not in ['normal','veterans','disability']:
                messages.add_message(request,messages.INFO,'身分別錯誤')
                return HttpResponseRedirect(f'/patient_edit/{patient.id}/')
            else:
                patient_form.save()
                messages.add_message(request,messages.SUCCESS,"病患資料已更新")
                return HttpResponseRedirect('/patient_manage/')
    else:
        patient_form=PatientForm(instance=patient)
    return render(request,'manager/patient_edit.html',locals())
def patient_delete(request,patient_id):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    try:
        patient=Info.objects.get(id=patient_id)
    except:
        raise Http404('查無該資料')
    patient_name=patient.user_name
    patient.delete()
    messages.add_message(request,messages.SUCCESS,f"病患「{patient_name}」已刪除")
    return HttpResponseRedirect('/patient_manage/')
def contact_manage(request):
    if 'user_name' not in request.session:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/login/')
    user_ID=request.session['user_ID']
    try:
        manager=Info.objects.get(user_ID=user_ID)
    except:
        raise Http404('查無該資訊')
    if not manager.can_manage:
        messages.add_message(request,messages.WARNING,'無權進入該界面')
        return HttpResponseRedirect('/info/')
    contacts=Contact.objects.all()
    return render(request, 'manager/contact_manage.html',locals())