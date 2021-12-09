from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class PdfForms(models.Model):
    Current_Date=models.CharField(max_length=100)
    Company_Name=models.CharField(max_length=500)
    Location=models.CharField(max_length=500)
    Role=models.CharField(max_length=200)
    Experience=models.CharField(max_length=200,null=True,blank=True)
    # job_Description=models.TextField(max_length=2000,null=True,blank=True)
    job_Description = RichTextField(blank=True,null=True)
    Email_link=models.CharField(max_length=500)
    mail_to=models.CharField(max_length=500,default="nikhil.sharma@jobaaj.com")
    subject=models.CharField(max_length=500,default="blank")
    mail_body=models.TextField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.Company_Name




