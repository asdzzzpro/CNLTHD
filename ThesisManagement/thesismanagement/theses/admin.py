import hashlib

from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    exclude = ['thesis']


admin.site.register(Faculty)
admin.site.register(AcademicManager)
admin.site.register(Lecturer)
admin.site.register(Student, StudentAdmin)
admin.site.register(Major)
admin.site.register(Committee)
admin.site.register(Thesis)
admin.site.register(Criteria)