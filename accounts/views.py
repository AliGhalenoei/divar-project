from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate , logout
from django.views import View

from .models import *
from .forms import *
from .sms import send_otp

import random
# Create your views here.



class UserAuthenticationView(View):

    """
        In this view:
        The user's phone number is received, and a 6-digit code is sent to them.
        Then, the user's phone number is stored in sessions under the name (auth_info).
    """

    form_class = UserAuthenticationForm
    template_name = 'accounts/login/user_login.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        print('User',request.user)
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            create_code = random.randint(100000,999999)

            # create otp in database
            
            otp = OTP.objects.filter(phone = cd['phone']).exists()
            if otp:
                OTP.objects.first()
            else:
                OTP.objects.create(phone = cd['phone'],code=create_code)

            # connect to kavenegar services
            send_otp(cd['phone'] , create_code)

            # Save the phone number in the session. 
            request.session['auth_info'] = {
                'phone':cd['phone']
            }
            return redirect('veryfy')
        return render(request,self.template_name,{'form':form})


class UserVeryfyAccountView(View):

    """
        In this view:
        If the user has had an account before and enters the correct code, they will log in.
        Otherwise, they will register and then log in.
    """

    form_class = UserVeryfyAccountForm
    template_name = 'accounts/login/veryfy.html'

    def setup(self, request, *args, **kwargs):
        self.get_session_instance = request.session['auth_info']
        self.get_phone_instanse = OTP.objects.get(phone = self.get_session_instance['phone'])
        
        self.users_count = User.objects.all().count()
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        get_phone = self.get_phone_instanse
        code = OTP.objects.get(phone=get_phone)
        return render(request,self.template_name,{'form':self.form_class , 'get_phone':get_phone,'code':code.code})
    
    def post(self , request):

        # Get the previous stage session" 🔄
        get_phone = self.get_phone_instanse
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == get_phone.code:
                # Checking if the user already has an account."
                exists_user = User.objects.filter(phone = self.get_phone_instanse)
                
                # login user
                if exists_user.exists():
                    user = exists_user.first()
                    login(request,user)
                    get_phone.delete()
                    return redirect('home')
                else:
                    # register user and login
                    create_pass = f'user_{random.randint(10000,99999)}'
                    register_user = User.objects.create_user(
                        phone = self.get_phone_instanse,
                        username = f'User_{self.users_count + 1}',
                        password = create_pass
                    )
                    login(request,register_user)
                    get_phone.delete()
                    return redirect('home')
            else:
                return redirect('veryfy')
        return render(request,self.template_name,{'form':form})
    

class UserLogoutView(View):

    """ logout users """

    def get(self , request):
        logout(request)
        return redirect('home')


