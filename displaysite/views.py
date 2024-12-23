from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import fileupform
import os
import json
from datetime import datetime

# register account
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('cemail')
        password = request.POST.get('cpass1')
        confirm_password = request.POST.get('cpass2')
        
        if not all([username, email, password, confirm_password]):
            messages.info(request, 'Please Fill All FIeld')
            return redirect('register')
        else: 
            if password==confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, first_name=full_name, password=password)
                    messages.info(request, 'Register Successfull')
                    user.save()
                    return redirect('dash')
            else:
                messages.info(request, 'Password does not match')
                return redirect('register')  
    else:
        return render(request, 'register.html')

# login for users
def loginusr(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, "Your username or password might be wrong. Please try again.")
            return redirect('loginusr')
    return render(request, 'login.html')

# logout
@login_required(login_url='loginusr')
def logoutusr(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('loginusr')

# dashboard
@login_required(login_url='loginusr')
def dash(request):
    user_id = request.user.id
    
    count = Patient.objects.filter(personal_doc = user_id).count()
    newestpat = Patient.objects.filter(personal_doc = user_id, newest_update__isnull = False).order_by('-newest_update').first()
    if count != 0 and newestpat != None:
        critcount = Patient.objects.filter(critical_con = True, personal_doc = user_id).count()
        ekg_data = patientdata.objects.filter(pat_owner = newestpat.id).order_by('-up_date').first()
        phonelink = "wa.me/62" + str(newestpat.phone_num)[1:]
    else:
        critcount = 0
        newestpat = None
        ekg_data = None
        phonelink = None
        
    if ekg_data != None:
        ekgvolt = []
        with ekg_data.jsondata.open() as file:
            opfile = json.load(file)
            ekgvolt = opfile.get("ekg_voltages", [])
            custrange = list(range(1, len(ekgvolt)+1))
    else:
        ekgvolt = [0]
        custrange = [0]
            
    
    htmlpass = {
        "count" : count,
        "critcount" : critcount,
        "newestpat" : newestpat,
        "ekgvolt" : ekgvolt,
        "ekgtimes" : custrange,
        "phone" : phonelink
    }
    return render(request, 'dash.html', htmlpass)

#patient tab
@login_required(login_url='loginusr')
def patienttab(request):
    user_id = request.user.id
    
    pats = Patient.objects.filter(personal_doc = user_id).order_by("id")
    
    htmlpass = {
        "patients" : pats
    }
    
    return render(request, 'patientstab.html', htmlpass)

@login_required(login_url='loginusr')
def search_patient(request):
    user_id = request.user.id
    quest = request.GET.get('quest', '')
    
    resi = Patient.objects.filter(full_name__icontains = quest, personal_doc = user_id)
    
    htmlpass = {
        "patients" : resi,
        "query" : quest
    }

    return render(request, 'patientstab.html', htmlpass)

# add patients function for patients tab
@login_required(login_url='loginusr')
def addpatient(request):
    user = request.user
    
    patname = request.POST['patname']
    patnum = request.POST['patnum']
    
    patsv = Patient.objects.create(full_name = patname, personal_doc = user, phone_num = patnum)
    patsv.save()
    
    return redirect('patientstab')

# patients detail page
@login_required(login_url='loginusr')
def patientsdet(request, patid):
    user_id = request.user.id
    
    passpat = Patient.objects.get(pk = patid)
    ekg_data = patientdata.objects.filter(pat_owner = passpat.id).order_by('-up_date').first()
    phonelink = "wa.me/62" + str(passpat.phone_num)[1:]
    
    if ekg_data == None:
        ekgvolt = []
        custrange = []
    else:
        ekgvolt = []
        with ekg_data.jsondata.open() as file:
            opfile = json.load(file)
            ekgvolt = opfile.get("ekg_voltages", [])
            custrange = list(range(1, len(ekgvolt)+1))
            
    htmlpass = {
        "ekgvolt" : ekgvolt,
        "ekgtimes" : custrange,
        "phone" : phonelink,
        "patient" : passpat
    }
    
    return render(request, 'patientdetail.html', htmlpass)
    

    


# blink | just so i dont need to set '' as dash's link | one of my petpeeves
def blink(request):
    return redirect('dashboard')

# -------------------------------------------------------------------------------
# 4 development

@login_required(login_url='loginusr')
# dummy file up
def fileup(request):
    if request.method == "POST":
        form = fileupform(request.POST, request.FILES)
        patid = request.POST['username']
        
        if form.is_valid():            
            file = request.FILES['file']
            namesplit = os.path.splitext(file.name)
            filetype = namesplit[1].lower()
            
            if filetype == '.json':
                filesv = patientdata.objects.create(jsondata = file, pat_owner_id = patid, up_date = datetime.now())
                updpat = Patient.objects.get(pk = patid)
                updpat.newest_update = datetime.now()
                updpat.save()
                filesv.save()
                return redirect('dummyup')
            
    else:
        form = fileupform()
        
    file = patientdata.objects.filter()
        
    return render(request, 'dummyinput.html', {'form': form, 'data': file})

