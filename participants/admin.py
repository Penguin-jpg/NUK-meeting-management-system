from django.contrib import admin
from .models import Expert, StudentRepresentative, Teacher, Assistant, Professor


class ExpertAdmin(admin.ModelAdmin):
    list_display = ["identity", "user"]


class StudentRepresentativeAdmin(admin.ModelAdmin):
    list_display = ["identity", "user"]


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["identity", "user"]


class AssistantAdmin(admin.ModelAdmin):
    list_display = ["identity", "user"]


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ["identity", "user"]


admin.site.register(Expert, ExpertAdmin)
admin.site.register(StudentRepresentative, StudentRepresentativeAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Professor, ProfessorAdmin)
