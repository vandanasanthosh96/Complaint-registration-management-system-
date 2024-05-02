from django.shortcuts import get_object_or_404, render,redirect
from django.core.mail import send_mail
from CRMS.settings import EMAIL_HOST_USER
from .forms import PublicUserCreationForm
from django.contrib.auth.models import Group 
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import*
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Complaint, Staff

#login and signup 
def home(request):
    try:
        if request.user.is_authenticated:
            userGroup = Group.objects.get(user=request.user).name
            print(userGroup)
            if userGroup =='Public':
                return redirect('pubhome')
            elif  userGroup =='Officer':
                return (redirect('offhome'))
            elif userGroup=='Staff':
                return (redirect('staffhome'))
            return render(request,'home.html')
        else:
            return render(request,'home.html')
    except Exception as e:
        print(e )
        return redirect('login')
    
def sign_up(request):
    form=PublicUserCreationForm()
    return render(request,'signup.html',{'form':form})
     
def user_registration(request):
    try:
        if request.method == "POST":
            form = PublicUserCreationForm(request.POST)
            if form.is_valid():
                mail = form.cleaned_data['email']
                name = form.cleaned_data['name']
                idproof = form.cleaned_data['idproof']
                address = form.cleaned_data['address']
                mobile = form.cleaned_data['mobile']
                password = form.cleaned_data['password1']
                username = form.cleaned_data['username']
                user = form.save()
                user = authenticate(request, email=mail, password=password, username=username)
                if user is not None:
                    login(request, user)

                    publicobj = Public.objects.create(publicuser=user, name=name, idproof=idproof, address=address, mobile=mobile,email=mail)
                    publicobj.save()

                    group = Group.objects.get(name="Public")
                    user.groups.add(group)

                    return redirect('login')
                else:
                    form=PublicUserCreationForm()
                    return render(request,'signup.html',{'form':form})
        else:
            form = PublicUserCreationForm()

        return render(request, 'signup.html', {'form': form})

    except Exception as e:
        print(e)
        return render(request, 'signup.html', {'form': form})

def loginview(request):
    uname=request.POST['username']
    pwd=request.POST['password']
    user=authenticate(request,username=uname,password=pwd)
    if user is not None:
        login(request,user)
        return redirect('home')
    # else:
        # return render(request,"login.html",{"msg":"INVALID LOGIN "})
def logout_view(request):
    logout(request)
    return redirect("home")




#public dashboard
@login_required
def pub_dashboard(request):
    pub_name = Public.objects.get(publicuser=request.user).name
    return render(request,'pub_dashboard.html',{"name1":pub_name})

@login_required
def compreg_form(request):
    return render(request,'complaintreg.html')

@login_required
def complaintregsiter(request):
    try:
        comptype = request.POST['comptype']
        place_occurance = request.POST['place']
        date_occurance = request.POST['date']
        desc = request.POST['desc']
        user = request.user
        pub = Public.objects.get(publicuser=user)
        
        compobj = Complaint.objects.create(
            created_user=user,
            pub_user=pub,
            complainttype=comptype,
            place_occurance=place_occurance,
            Date_occurance=date_occurance,
            desc=desc
        )
        
        compobj.save()
        return render(request, "complaintreg.html", {"comp": "COMPLAINT REGISTERED SUCCESSFULLY"})
    except Exception as e:
        print(e)
        return render(request, "complaintreg.html", {"comp": "COMPLAINT REGISTRATION UNSUCCESSFUL"})

@login_required
def mycomplaints(request):
    compobj=Complaint.objects.filter(created_user=request.user)
    return render(request,'mycomplaints.html',{'objs':compobj})

@login_required
def delete_complaint(request,complaint_id):
    delobj = get_object_or_404(Complaint, id=complaint_id)
    delobj.delete()
    messages.success(request, "Complaint deleted successfully")
    return redirect('pubhome')  
    
    # else:
    #     messages.error(request, "Cannot delete complaint ") 

@login_required
def pubprofile(request):
    pubobj = Public.objects.filter(publicuser_id=request.user.id)
    return render(request,'pubprofile.html',{'propub':pubobj})

@login_required
def todashboard(request):
    return render(request,'pub_dashboard.html')

#officerdash

@login_required
def officerdash(request):
    off_name = Officer.objects.get(officeruser=request.user).name
    staffs = Staff.objects.all()
    return render(request,'officerdash.html',{"name2":off_name,'staffs': staffs})


@login_required
def retoffdash(request):
    return render(request,'officerdash.html')

@login_required
def logoutoff(request):
    return redirect('logout')

@login_required
def officerprofile(request):
    offobj=Officer.objects.filter(officeruser_id=request.user.id)
    return render(request,'officerprofile.html',{'pro3':offobj})

@login_required
def allcomplaint(request):
    staff_id = request.GET.get('staff_id')
    staffs = Staff.objects.all()
    if staff_id:
        staff = get_object_or_404(Staff, id=staff_id)
        allcompobj = Complaint.objects.filter(staff=staff)
    else:
        allcompobj = Complaint.objects.all()
    return render(request, 'allcomplaints.html', {'objs': allcompobj, 'staffs': staffs})

@login_required
def assign_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        status = request.POST.get('status', '').lower()
        
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            messages.error(request, "Invalid staff ID")
            return redirect('home')  
        
        if status not in ['inprogress','new', 'resolved', 'closed','invalid','pending']:  
            messages.error(request, "Invalid status")
            return redirect('home') 
        
        complaint.assigned_staff = staff
        complaint.status = status.capitalize()  # Capitalize status before saving
        complaint.save()    
        messages.success(request, "Complaint assigned successfully")
        return redirect('offhome') 
    
    return render(request, 'home.html', {'complaint': complaint})

#staff dashboard

@login_required
def staffdash(request):
    staff_name = Staff.objects.get(user=request.user).name
    return render(request,'staffdash.html',{"name3": staff_name})

@login_required
def newcomstaff(request):
    staff_user_id = request.user.id
    staff_instance = Staff.objects.get(user_id=staff_user_id)
    ass_comp = Complaint.objects.filter(assigned_staff_id=staff_instance.id)
    return render(request, 'newcomstaff.html', {'ass_comp': ass_comp})

@login_required
def status_update_view(request, complaint_id):
    item = Complaint.objects.get(id=complaint_id)
    try:
        if request.method == 'POST':
            status = request.POST.get('status', '').lower()    
            if status not in ['inprogress','new','resolved', 'closed','invalid','pending']:  
                    messages.error(request, "Invalid status")
                    return redirect('staffhome')
            else:
                item.status = status.capitalize()  # Capitalize status before saving
                item.save() 
                pub_user=item.pub_user
                if pub_user:
                    print(f"Public user Email:{pub_user.email}")
                    recipient=pub_user.email
                    subject="Complaint status "
                    message=f"Complaint status updated to{item.status}"
                    send_mail(subject,message,EMAIL_HOST_USER,[recipient])
                else:
                    print("No public user associated with this complaint.")

                messages.success(request, "Complaint status updated")
                return redirect('staffhome') 
        return render(request,'newcomstaff.html')
    except Exception as e:
            return render(request,'newcomstaff.html')

@login_required
def staffprofile(request):
    staffobj = Staff.objects.filter(user_id=request.user.id)
    return render(request,'staffprofile.html',{'pro1':staffobj})

@login_required
def retstaff(request):
    return render(request,'staffdash.html')

@login_required
def logoutstaff(request):
    return redirect('logout')


            


