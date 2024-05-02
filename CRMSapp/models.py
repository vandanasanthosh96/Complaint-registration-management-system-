from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Master(models.Model):
    create_date=models.DateTimeField(auto_now_add=True)
    isactive=models.BooleanField(default=True,verbose_name="Active")
    created_user=models.ForeignKey(User,blank=True,on_delete=models.CASCADE,null=True)

    class Meta:
        abstract=True
        ordering=['-isactive']

class Transaction(models.Model):
    create_date=models.DateTimeField(auto_now_add=True)
    created_user=models.ForeignKey(User,blank=True,on_delete=models.CASCADE)

    class Meta:
        abstract=True


class Public(Master):
    publicuser=models.OneToOneField(User,on_delete=models.CASCADE,related_name='publicuser')
    name=models.CharField(max_length=30,verbose_name='Public')
    # idprooftype=[
    #     ('Aadhar','Aadhar'),
    #     ('Voters Id','Voters Id'),
    #     ('PAN','PAN'),
           
    # ]
    idproof=models.CharField(max_length=15)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=12)
    email=models.EmailField()

    def __str__(self):
      return self.name

class Officer(Master):
    officeruser=models.OneToOneField(User,on_delete=models.CASCADE,related_name='officeruser')
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=40,verbose_name='Jurisdiction')
    designation = models.CharField(max_length=40)
    mobile = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class Staff(Master):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=40,verbose_name='Jurisdiction')
    designation = models.CharField(max_length=40)
    mobile = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class Complaint(Transaction):
    COMPLAINT_TYPE_CHOICES=[
        ('Theft','Theft'),
        ('Missing','Missing'),
        ('Public Nuissance','Public Nuissance'),
        ('Attack against women','Attack against women'),
       
    ]

    STATUS_CHOICES = [
        ('New', 'New'),
        ('Invalid', 'Invalid'),
        ('InProgress', 'InProgress'),
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    pub_user = models.ForeignKey(Public, blank=True, on_delete=models.CASCADE)
    complainttype = models.CharField(max_length=40, choices=COMPLAINT_TYPE_CHOICES)
    file_up = models.FileField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='New')
    desc = models.TextField()
    assigned_staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    Date_occurance=models.DateTimeField(auto_now_add=True)
    place_occurance=models.TextField(default=None)
    