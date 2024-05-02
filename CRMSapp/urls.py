from django.urls import path
from django.contrib import admin
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('signup',views.sign_up,name='signup'),
    path('accounts/signup',views.user_registration),
    path('accounts/login/',views.loginview,name='login'),
    path('logout',views.logout_view,name='logout'),

    path('my-crms-secret-admin-url/',admin.site.urls,name='admin'),    
    path('public/dashboard',views.pub_dashboard,name='pubhome'),
    path('pubprofile',views.pubprofile),
  
#public complaint
    path('compreg',views.compreg_form,name='compreg'),
    path('mycomplaints',views.mycomplaints,name='mycomplaints'), 
    path('delete_complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('register_complaint',views.complaintregsiter),
    path('Dashboard',views.todashboard,name='dash'),

#officer dashboard
    path('officer/dashboard',views.officerdash,name='offhome'),
    path('officer/allcomplaint/', views.allcomplaint),
    path('officer/assign_complaint/<int:complaint_id>/', views.assign_complaint, name='assign_complaint'),
    path('officer/retoffdash',views.retoffdash),
    path('officerprofile',views.officerprofile,name='officerprofile'),
    path('officer/logout',views.logoutoff),

#staff dashboard
    path('staff/dashboard',views.staffdash,name='staffhome'),
    path('staffprofile',views.staffprofile),
    path("staff/newcomplaint/",views.newcomstaff,name='newcomstaff'),
    path('statusupdate/<int:complaint_id>/',views.status_update_view, name='statusupdate'),
    path('staff/retoffdash',views.retstaff),
    path('staff/logout',views.logoutstaff),

]
