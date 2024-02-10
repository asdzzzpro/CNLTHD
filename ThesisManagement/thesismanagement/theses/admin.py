from django.contrib import admin
from django.urls import path
from .models import *


class CourseAppAdminSite(admin.AdminSite):
    site_header = "HỆ THỐNG QUẢN LÝ KHÓA LUẬN TỐT NGHIỆP"

    # def get_urls(self):
    #     return [
    #                path('course-stats/', self.stats_view)
    #            ] + super().get_urls()

    # def stats_view(self, request):
    #     return TemplateResponse(request, 'admin/stats.html', {
    #         "stats": dao.count_courses_by_cate_id()
    #     })


class UserAdmin(admin.ModelAdmin):
    fields = ['avatar', 'first_name', 'last_name', 'username', 'password', 'email', 'faculty']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)

        super().save_model(request, obj, form, change)


class AcademicManagerAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        obj.role = UserRole.ACADEMIC_MANAGER

        super().save_model(request, obj, form, change)


class LecturerAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        obj.role = UserRole.ACADEMIC_MANAGER.value

        super().save_model(request, obj, form, change)


class StudentAdmin(UserAdmin):
    fields = UserAdmin.fields + ['major']
    exclude = ['thesis']

    def save_model(self, request, obj, form, change):
        obj.role = UserRole.ACADEMIC_MANAGER

        super().save_model(request, obj, form, change)


admin_site = CourseAppAdminSite(name='MyApp')


admin_site.register(Faculty)
admin_site.register(AcademicManager, AcademicManagerAdmin)
admin_site.register(Lecturer, LecturerAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Major)
admin_site.register(Committee)
admin_site.register(Thesis)
admin_site.register(Criteria)