from django.contrib import admin
from .models import Profile, ReturnList, Document

# Register your models here.
admin.site.register(Profile)
admin.site.register(ReturnList)
admin.site.register(Document)