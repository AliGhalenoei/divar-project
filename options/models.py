from django.db import models

from accounts.models import User

from content.models import Advertisement
# Create your models here.



class SaveAdvertisement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_save')
    advertisement = models.ForeignKey(Advertisement,on_delete=models.CASCADE,related_name='advertisement_save')

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f'{self.user} Save advertisement {self.advertisement}'
    
class NoteAdvertisement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_note')
    advertisement = models.ForeignKey(Advertisement,on_delete=models.CASCADE,related_name='advertisement_note')
    note = models.TextField(null=True , blank=True)

    class Meta:
        ordering = ['-id']
        
    def __str__(self) -> str:
        return f'{self.user} create note advertisement {self.advertisement}'


class ViewAdvertisement(models.Model):
    advertisement = models.ForeignKey(Advertisement,on_delete=models.CASCADE,related_name='advertisement_view')
    user_ip = models.GenericIPAddressField(null=True,blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        unique_together = ('advertisement', 'user_ip')