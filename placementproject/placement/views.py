from django import db
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse

#models
from .models import PdfForms
# modelform
from .forms import PdfFormsform

# authorzatioin
import placement
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Email
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

# pdf file download and send_mail
from textwrap import wrap
from datetime import datetime

from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa

# login page

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('placement:index')
        else:
            messages.info(request,'invalid credientials')
            return redirect('/login/')
    else:
        return render(request,"login.html")

# register

# def register(request):
    
#     if request.method == 'POST': 
#         if request.POST['username'] and request.POST['first_name'] and request.POST['email'] and request.POST['pass1'] and request.POST['pass2'] :
#             username = request.POST['username']
#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']
#             email = request.POST['email']
#             pass1 = request.POST['pass1']
#             pass2 = request.POST['pass2'] 
#             if pass1 == pass2:
#                 if User.objects.filter(username=username).exists():
#                     messages.info(request,'User already exists with that username.')
#                     return redirect('placement:register')
                
#                 elif User.objects.filter(email=email).exists():
#                     messages.info(request,'Email already registered')
#                     return redirect('placement:register')


#                 else:
#                     user = User.objects.create_user(username=username, password=pass1,email=email,first_name=first_name,last_name=last_name)
#                     user.save()
#                     # print('user created')
#                     return redirect('placement:login')

#             else:
#                 messages.info(request,'Password does not match')
#                 return redirect('placement:register')

#         else:
#             messages.info(request,"Invalid crediantials")
#             return redirect('placement:register')
            
#     else:
#         return render(request,"register.html") 

# logout

def logout(request):
    auth.logout(request)
    return redirect("/")


# Create your views here.
@login_required(login_url="/login/")
def index(request):
    if request.method=='POST':
        if request.POST['Company_Name'] and request.POST['Location'] and request.POST['Role']and request.POST['exp'] and request.POST['Email_link']:
            now = datetime.now()
            CDate = now.strftime("%d/%m/%Y")
            CName = request.POST.get('Company_Name')
            Location= request.POST.get('Location')
            Role = request.POST.get('Role')
            jobDescription = request.POST.get('job_Description')
            Emaillink = request.POST.get('Email_link')
            Experience =  request.POST.get('exp')
            
            # saving data in db
            obj=PdfForms(Current_Date=CDate,Company_Name=CName,Location=Location,Role=Role,job_Description=jobDescription,Email_link=Emaillink,Experience=Experience)
            obj.save()

            # creating pdf
            try:
                Emaillink = "\n".join(wrap(Emaillink,width=80))
                lead = {'now':now, 'CDate':CDate,'CName':CName,'Location':Location,'Role':Role,'jobDescription':jobDescription,'Emaillink':Emaillink,'Experience':Experience}
                context={"lead":lead}
                # print(context)
                # return render(request,'preview.html',context=context)

                template_path = 'preview.html'
                # Create a Django response object, and specify content_type as pdf
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                # find the template and render it.
                template = get_template(template_path)
                html = template.render(context)
                # create a pdf
                pisa_status = pisa.CreatePDF(
                   html, dest=response)
                # if error then show some funy view
                if pisa_status.err:
                   return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            except:
                messages.error(request,'PDF Error')
                return redirect('placement:index')
        else:
            messages.error(request,'Invalid Details')
            return redirect('placement:index')
    else:
        return render(request,'index.html',{"form":PdfFormsform()})

# pdf preview
def preview(request):
    return render(request,'preview.html')
# mail function

def mail_pdf(request):
    mailto = request.POST.get('mailto')
    subject = request.POST.get('subject')
    mail_body = request.POST.get('mail_body')
    files = request.FILES.getlist('attach')
    print(mailto)
    obj=PdfForms(mail_to=mailto,subject=subject,mail_body=mail_body)
    obj.save()
    mail = EmailMessage(subject, mail_body, settings.DEFAULT_FROM_EMAIL, [mailto],cc=['contact@jobaaj.com','ishika.singhal@jobaaj.com'])
    for f in files:
        mail.attach(f.name, f.read(), f.content_type)
    mail.send()
    messages.success(request,'mail sent')
    return redirect('placement:index')