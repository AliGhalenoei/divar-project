from django.db.models.signals import post_save

from .models import UserProfile , User

def create_profile_signal(sender , **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(
            user = kwargs['instance']
        )
post_save.connect(receiver=create_profile_signal , sender = User)