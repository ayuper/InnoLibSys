from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Document(models.Model):
	type_options = (
		(0, "Book"),
		(1, "Article"),
		(2, "Audio-Video Material"),
	)
	document_type = models.IntegerField(choices=type_options)
	published_date = models.DateField()
	overdue_date = models.DateField(null=True)
	title = models.CharField(max_length=100, default=None)
	user = models.ForeignKey(User, related_name='documents', on_delete=models.CASCADE, null=True)
	to_return = models.BooleanField(default=False)
	best_seller = models.BooleanField(default=False)
	authors = models.CharField(max_length=200,default=None, null=True)
	price = models.IntegerField(default=0)
	def get_absolute_url(self):
		return reverse('manage-document', kwargs={'id':self.id})

class ReturnList(models.Model):
	document = models.OneToOneField(Document, on_delete=models.CASCADE)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class Profile(models.Model):
	type_options = (
		(0, "Faculty"),
		(1, "Student"),
		(2, "Visiting Professor"),
	)
	patron_type = models.IntegerField(choices=type_options, default=0)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	librarian = models.BooleanField(default=False)
	phone_number = models.CharField(max_length=20, default=None, null=True)
	adress = models.CharField(max_length=50, default=None, null=True)
	fine = models.IntegerField(default=0)
	def get_absolute_url(self):
		return reverse('manage-patron', kwargs={'id':self.id})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()