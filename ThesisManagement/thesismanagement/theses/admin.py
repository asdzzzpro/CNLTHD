import hashlib

from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    exclude = ['thesis']

    def save_model(self, request, obj, form, change):
        obj.password = hashlib.md5(form.cleaned_data["password"].encode("utf-8")).hexdigest()
        super().save_model(request, obj, form, change)


admin.site.register(Faculty)
admin.site.register(AcademicManager)
admin.site.register(Lecturer)
admin.site.register(Student, StudentAdmin)
admin.site.register(Major)
admin.site.register(Committee)
admin.site.register(Thesis)
admin.site.register(Criteria)