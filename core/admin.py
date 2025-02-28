from django.contrib import admin
from .models import Role, CustomUser,News,StudyMaterial

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(News)
admin.site.register(StudyMaterial)