from django.contrib import admin
from .models import Expert, StudentRepresentative, Teacher, Assistant, Professor

# Register your models here.
admin.site.register(Expert)
admin.site.register(StudentRepresentative)
admin.site.register(Teacher)
admin.site.register(Assistant)
admin.site.register(Professor)