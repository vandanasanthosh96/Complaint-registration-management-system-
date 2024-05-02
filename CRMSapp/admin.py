from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from.models import *
# Register your models here.

class MasterAdmin(admin.ModelAdmin):
    exclude=['created_user']

    def has_delete_permission(self, request,obj=None):
        return False
    
    def save_model(self,request,obj,form,change):
        obj.created_user=request.user
        super().save_model(request,obj,form,change)

class TransactionAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request,obj=None):
        return False
    
    def save_model(self,request,obj,form,change):
        obj.created_user=request.user
        super().save_model(request,obj,form,change)

class PublicAdmin(MasterAdmin):
    list_display=['name','isactive']


class OfficerAdmin(MasterAdmin):
    list_display=['name','isactive']

class StaffAdmin(MasterAdmin):
       list_display=['name','isactive']

class ComplaintAdmin(TransactionAdmin):
    list_display=['pub_user','complainttype','status','assigned_staff','place_occurance']

admin.site.register(Public,PublicAdmin)
admin.site.register(Officer,OfficerAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Complaint,ComplaintAdmin)