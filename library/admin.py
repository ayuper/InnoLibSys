from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(ReturnList)
admin.site.register(Document)
admin.site.register(Copy)
admin.site.register(DocumentQueue)
admin.site.register(Notifications)