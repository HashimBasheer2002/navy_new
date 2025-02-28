from django.contrib import admin
from .models import Role, CustomUser,News

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(News)
