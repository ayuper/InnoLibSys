from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    librarian = models.BooleanField(default=False)
    def get_absolute_url(self):
    	return reverse('manage-patron', kwargs={'id':self.id})

class Document(models.Model):
	document_type = models.IntegerField()
	published_date = models.DateTimeField()
	overdue_date = models.DateTimeField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()