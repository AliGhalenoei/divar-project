from django.db import models

from accounts.models import User
# Create your models here.


class City(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    

class Category(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)

    sub = models.ForeignKey('self',on_delete=models.CASCADE , related_name='sub_cate',null=True,blank=True)
    is_sub = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Advertisement(models.Model):

    STATUS_ADVERTISEMENT = (
        ('new','نو'),
        ('like-new','در حد نو'),
        ('used','کارکرده'),
        ('need-repair','نیاز به تعمیر')
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_advertisement')
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='city_advertisement')
    category = models.ManyToManyField(Category,related_name='cate_advertisement')

    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='advertisements/')
    status = models.CharField(max_length=11,choices=STATUS_ADVERTISEMENT)
    price = models.BigIntegerField()
    fixed_price = models.BooleanField(default=False)
    wiling_excheng = models.BooleanField(default=False)

    slug = models.SlugField(max_length=255,unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title
    
    def user_can_save(self , user):
        user = user.user_save.filter(advertisement = self).exists()
        if user:
            return True
        return False
    

    




