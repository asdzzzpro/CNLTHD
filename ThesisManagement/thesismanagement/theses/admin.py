from django.contrib import admin
from .models import *


class CourseAppAdminSite(admin.AdminSite):
    site_header = "HỆ THỐNG QUẢN LÝ KHÓA LUẬN TỐT NGHIỆP"


class UserAdmin(admin.ModelAdmin):
    fields = ['avatar', 'first_name', 'last_name', 'username', 'password', 'email', 'faculty']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)

        super().save_model(request, obj, form, change)


class AcademicManagerAdmin(UserAdmin):

    def save_model(self, request, obj, form, change):
        obj.role = UserRole.ACADEMIC_MANAGER.value

        super().save_model(request, obj, form, change)


class LecturerAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        obj.role = UserRole.LECTURER.value

        super().save_model(request, obj, form, change)


class StudentAdmin(UserAdmin):
    fields = UserAdmin.fields + ['major']
    exclude = ['thesis']

    def save_model(self, request, obj, form, change):
        obj.role = UserRole.STUDENT.value

        super().save_model(request, obj, form, change)


class ThesisAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


admin_site = CourseAppAdminSite(name='MyApp')

admin_site.register(Faculty)
admin_site.register(AcademicManager, AcademicManagerAdmin)
admin_site.register(Lecturer, LecturerAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Major)
admin_site.register(Committee)
admin_site.register(Thesis, ThesisAdmin)
admin_site.register(Criteria)