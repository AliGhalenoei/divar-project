from django.views import View
from django.core.mail import send_mail
from django.shortcuts import render , redirect
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *

import uuid


class SaveAdvertisementView(LoginRequiredMixin,View):

    def get(self , request , advertisement_id):
        user = request.user
        advertisement = Advertisement.objects.get(id = advertisement_id)
        
        check = SaveAdvertisement.objects.filter(user = user , advertisement = advertisement)
        if check.exists():
            check.delete()
            return redirect('detail_advertisement' , advertisement.slug)
        else:
            SaveAdvertisement.objects.create(user = user , advertisement = advertisement)
            return redirect('detail_advertisement' , advertisement.slug)
        

class ViewAdvertisementView(View):

    def get(self , request , advertisement_id):
        user_ip = request.META.get('REMOTE_ADDR')
        advertisement = Advertisement.objects.get(id = advertisement_id)
        check=ViewAdvertisement.objects.filter(advertisement=advertisement,user_ip = user_ip).exists()
        if check:
            return redirect('detail_advertisement' , advertisement.slug)
        else:
            ViewAdvertisement.objects.create(advertisement=advertisement,user_ip = user_ip)
            return redirect('detail_advertisement' , advertisement.slug)

    

class DeleteAdvertisementNoteView(LoginRequiredMixin,View):

    def get(self , request , note_id):
        user = request.user
        note = NoteAdvertisement.objects.get(id = note_id)
        note.delete()
        return redirect('advertisement_notes')
    

class CreateAdvertisementView(LoginRequiredMixin,View):

    form_class = CreateAdvertisementForm
    template_name = 'options/pages/create_advertisement.html'

    def get(self , request):
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self , request):
        user = request.user
        uniqued_slug = str(uuid.uuid4())
        form = self.form_class(request.POST , request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.user = user
            post.slug = uniqued_slug
            post.save()
            post.category.set(cd['category'])
            
            return redirect('home')
        return render(request,self.template_name,{'form':form})
    

class DeleteAdvertisementView(LoginRequiredMixin,View):

    def setup(self, request, *args, **kwargs):
        self.advertisement_instance = Advertisement.objects.get(id = kwargs['advertisement_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        advertisement = self.advertisement_instance
        if not advertisement.user.id == request.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request , *args , **kwargs):
        advertisement = self.advertisement_instance
        advertisement.delete()
        return redirect('user_profile' , request.user.id)
    

class ContactUsView(LoginRequiredMixin,View):

    template_name = 'options/pages/contact.html'
    form_class = ContactUsForm

    def get(self , request):
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self , request):
        user = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            msg = """
                    User: {0} \n
                    Subject: {1} \n
                    Message: {2}
                  """.format(user,cd['subject'],cd['message'])
            send_mail(cd['subject'],msg,'testpass935@gmail.com',['testpass935@gmail.com'],fail_silently=False)
            return redirect('home')
        return render(request,self.template_name,{'form':form})

