from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import datetime
from django.db import models
from django.db.models import Q

from django.core.cache import cache


from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    STATUS = (
        ('Male','Male'),
        ('Female','Female')
    )
    user = models.OneToOneField(User, null=True, blank= True, on_delete=models.CASCADE)
    age = models.IntegerField(null=True,blank = True,default='0')
    gender = models.CharField(max_length =200,null=True, choices=STATUS,default='',blank = True)
    state = models.CharField(max_length=200, null=True,default='',blank = True)
    country = CountryField(blank_label='select country',null=True,blank = True)
    bio = models.TextField(max_length=1000, null=True,default='',blank = True)
    profile_pic = models.ImageField(default="user.png",null=True, blank = True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    
    def __str__(self):
    	return f"{self.user.username} Profile" 
        
    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)
    
    @property
    def is_online(self):
        if self.last_seen():
            now = datetime.datetime.now()- datetime.timedelta(minutes=15)
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else: 
            return False








class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    
    timestamp    = models.DateTimeField(auto_now=True)
    
    objects      = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False

   


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now=True)
    is_read     = models.BooleanField(default=False)

    

    