from django.db.models.signals import post_save

from django.contrib.auth.models import User
from .models import Profile
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('Profile created')

post_save.connect(create_profile, sender=User)

def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()
        print('Profile Updated!')


post_save.connect(update_profile, sender=User)