from django.contrib import admin

# Register your models here.
from .models import BlogPost, UserPayments


admin.site.register(BlogPost)
admin.site.register(UserPayments)