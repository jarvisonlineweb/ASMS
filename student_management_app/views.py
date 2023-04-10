# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.models import CustomUser,OTP_system
from django.core.mail import EmailMultiAlternatives
from random import randint
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password



def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def forget_password(request):
    if request.method == "GET":
        print('this is forget page')
        return render(request, 'forget_password.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email):
            print('data  write')
            print(';;;;;', email)
            otp = randint(100000, 999999)
            OTP = str(otp)

            data_pre = OTP_system.objects.filter(email=email).first()
            print(data_pre)
            if data_pre:
                data_pre.delete()
                OTP_save = OTP_system(email=email, OTP=OTP)
                OTP_save.save()
            else:
                OTP_save = OTP_system(email=email, OTP=OTP)
                OTP_save.save()


            # email is staring ..........
            # app skoimepzguahnumz

            subject = 'welcome to abc School '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            html_message = render_to_string("send_mail.html", {'otp': OTP})
            text_content = strip_tags(html_message)
            email1 = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            email1.attach_alternative(html_message, "text/html")
            email1.send()

            return render(request, 'set_new_pasword.html',  {"email": email})

        else:
            messages.error(request, "Invalid Email/Username")
        return render(request, 'forget_password.html')

def set_new_password(request):
    if request.method == 'GET':
        return render(request, 'set_new_pasword.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        # OTP = request.POST.get('OTP')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            OTP = OTP_system.objects.get(email=email)
            if OTP:
                print('okok')
                user = CustomUser.objects.get(email=email)
                password = make_password(new_password)
                user.password = password
                user.save()
                print('done...')
                messages.success(request, "Reset Password Successfully.")
                return redirect('login')
            else:
                messages.error(request, "**Enter Valid Password")
        else:
            messages.error(request, "**Passwords are not same")
        return render(request, 'set_new_pasword.html')