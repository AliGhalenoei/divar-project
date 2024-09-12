from django import forms

from options.models import NoteAdvertisement
from content.models import Advertisement


class NoteAdvertisementForm(forms.Form):
    note = forms.CharField(label='note',widget=forms.Textarea())



class CreateAdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('city' , 'category' , 'title' , 'body' , 'image' , 'fixed_price' , 'wiling_excheng' , 'status' , 'price')


class ContactUsForm(forms.Form):

    STATUS = (
        ('a','پرداخت و موارد مالی'),
        ('b','کلاهبرداری، مزاحمت یا گزارش تخلف'),
        ('c','حساب کاربری، تایید هویت، چت یا تماس'),
        ('d','سایر موارد')
    )

    subject = forms.ChoiceField(choices=STATUS)
    message = forms.CharField(widget=forms.Textarea())