from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100,default='')
    city = models.CharField(max_length=20,default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    is_live = models.BooleanField(default=True)
    token = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.user.username

    def as_json(self):
        return{
            "description":self.description,
            "city":self.city,
            "website":self.website,
            "phone":self.phone,
            "username":self.user.username,
            "first_name":self.user.first_name,
            "last_name":self.user.last_name,
            "email":self.user.email,
        }

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)


