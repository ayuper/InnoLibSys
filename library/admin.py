from django.contrib import admin
from .models import Profile, ReturnList, Document, Copy

# Register your models here.
admin.site.register(Profile)
admin.site.register(ReturnList)
admin.site.register(Document)
admin.site.register(Copy)