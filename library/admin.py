from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Teacher, Student, BookAuthor, BookCategory, BookPublisher, BookLanguage, Book

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('email', 'first_name', 'last_name', 'phone_no', 'is_admin', 'is_teacher', 'is_student')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_admin', 'is_teacher', 'is_student'),
        }),
    )
    list_display = ('username', 'email', 'first_name','last_name', 'phone_no', 'is_admin', 'is_teacher', 'is_student')
    list_filter = ('is_admin', 'is_teacher', 'is_student')
    search_fields = ('username', 'email', 'phone_no', 'first_name','last_name')
    ordering = ('first_name','last_name')  # Use actual fields for ordering
    

# Teacher Admin
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name','last_name', 'phone_no', 'employee_id', 'level', 'class_name', 'teacher_type', 'employment_status', 'department', 'subject')
    search_fields = ('user__username', 'user__email', 'user__phone_no', 'employee_id', 'user__first_name', 'user__last_name')
    list_filter = ('level', 'subject', 'department')

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    def phone_no(self, obj):
        return obj.user.phone_no
    phone_no.short_description = 'Phone Number'

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'

# Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name','last_name', 'phone_no', 'registration_no', 'level', 'year', 'faculty')
    search_fields = ('user__username', 'user__email', 'user__phone_no', 'registration_no', 'user__first_name', 'user__last_name')
    list_filter = ('level', 'faculty')

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    def phone_no(self, obj):
        return obj.user.phone_no
    phone_no.short_description = 'Phone Number'

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(BookAuthor)
admin.site.register(BookCategory)
admin.site.register(BookPublisher)
admin.site.register(BookLanguage)
admin.site.register(Book)
