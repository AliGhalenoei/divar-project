from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import render , redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *

from options.forms import NoteAdvertisementForm 
from options.models import SaveAdvertisement , NoteAdvertisement , ViewAdvertisement
# Create your views here.


class HomeView(View):

    form_class = SearchAdvertisementForm
    template_name = 'content/pages/home.html'

    def setup(self, request, *args, **kwargs):
        self.citys_instance = City.objects.all()
        self.categorys_instance = Category.objects.all()
        self.advertisements_instance = Advertisement.objects.all().order_by('?')
        return super().setup(request, *args, **kwargs)

    def get(self , request , slug_city=None , slug_category=None):
        citys = self.citys_instance
        categorys = self.categorys_instance
        advertisements = self.advertisements_instance
        
        # Filter advertisements by category
        if slug_category:
            filter_category = self.categorys_instance.get(slug = slug_category)
            advertisements = self.advertisements_instance.filter(category = filter_category)

        # Filter advertisements by city
        if slug_city:
            filter_city = self.citys_instance.get(slug = slug_city)
            advertisements = self.advertisements_instance.filter(city = filter_city)

        # search advertisements
        if request.GET.get('search'):
            advertisements = advertisements.filter(title__icontains = request.GET['search'])

        return render(request,self.template_name,{
            'citys':citys,
            'categorys':categorys,
            'advertisements':advertisements,
            'form':self.form_class
        })
   
    
class DetailAdvertisementsView(View):

    form_class = NoteAdvertisementForm
    template_name = 'content/pages/detail.html'

    def setup(self, request, *args, **kwargs):
        self.advertisement_instance = Advertisement.objects.get(slug = kwargs['slug_advertisement'])

        self.note_instanse = None
        if request.user.is_authenticated:
            check = NoteAdvertisement.objects.filter(user = request.user , advertisement = self.advertisement_instance)
            if check.exists():
                self.note_instanse = NoteAdvertisement.objects.get(user = request.user , advertisement = self.advertisement_instance)

        return super().setup(request, *args, **kwargs)

    def get(self , request , *args, **kwargs):
        user = request.user
        can_save = False

        if request.user.is_authenticated and self.advertisement_instance.user_can_save(user):
            can_save = True

        return render(request,self.template_name,{
            'advertisement':self.advertisement_instance,
            'can_save':can_save,
            'note':self.note_instanse
        })
    
    @method_decorator(login_required)
    def post(self , request , *args, **kwargs):
        user = request.user
        advertisement = self.advertisement_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            check = NoteAdvertisement.objects.filter(user = user, advertisement = advertisement)

            if check.exists():
                # update note
                get_note = check.first()
                get_note.note = cd['note']
                get_note.save()
                return redirect('detail_advertisement', advertisement.slug)
            else:
                # create note
                NoteAdvertisement.objects.create(
                    user = user,
                    advertisement = advertisement,
                    note = cd['note']
                )
                return redirect('detail_advertisement', advertisement.slug)
        return render(request,self.template_name,{'form':form})
    

class AdvertisementsSaveView(LoginRequiredMixin,View):

    template_name = 'content/pages/page_save_advertisement.html'

    def get(self , request):
        user = request.user
        advertisements =  SaveAdvertisement.objects.filter(user = user)
        return render(request,self.template_name,{'advertisements':advertisements})
        

class AdvertisementsNoteView(LoginRequiredMixin,View):

    template_name = 'content/pages/page_note_advertisement.html'  

    def get(self , request):
        user = request.user
        notes =  NoteAdvertisement.objects.filter(user = user)
        return render(request,self.template_name,{'notes':notes})  
    

class RecentVisitsView(View):

    template_name = 'content/pages/page_recent_visit.html'  

    def get(self , request):
        user = request.user
        visits =  ViewAdvertisement.objects.all()
        return render(request,self.template_name,{'visits':visits})  
    

class UserProfileView(LoginRequiredMixin,View):

    template_name = 'content/pages/user_profile.html'

    def get(self , request , user_id):
        user = UserProfile.objects.get(user = user_id)
        advertisements = Advertisement.objects.filter(user = request.user)
        return render(request,self.template_name,{'user':user,'advertisements':advertisements})
    

class UpdateProfileView(LoginRequiredMixin,View):

    form_class = UpdateProfileForm
    template_name = 'content/pages/update_profile.html'

    def setup(self, request, *args, **kwargs) -> None:
        self.profile_instance = UserProfile.objects.get(user = kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        profile = self.profile_instance
        if not profile.user.id == request.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request , *args , **kwargs):
        profile = self.profile_instance
        return render(request,self.template_name,{'profile':profile})
    
    def post(self , request , *args , **kwargs):
        profile = self.profile_instance
        form = self.form_class( request.POST , request.FILES , instance=profile)

        if form.is_valid():
            form.save()
            return redirect('user_profile' , profile.user.id)
        return render(request,self.template_name,{'form':form})
