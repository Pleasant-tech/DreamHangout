import django_filters
from django_filters import CharFilter
from django.contrib.auth.models import User

from .models import *

class ProfileFilter(django_filters.FilterSet):
    state = CharFilter(field_name="state",lookup_expr ='icontains',label='')
    class Meta:
        model = Profile
        fields = 'age','gender','state','country'
       
    def __init__(self, *args, **kwargs):
    	super(ProfileFilter,self).__init__(*args, **kwargs)
    	self.filters['age'].label=""
    	self.filters['gender'].label=""
    	self.filters['state'].label=""
    	self.filters['country'].label=""


        