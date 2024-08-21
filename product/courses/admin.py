from django.contrib import admin

from courses.models import Course, Group, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'start_date', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('title', 'author')
    ordering = ('-start_date',)
    fieldsets = (
        (None, {'fields': ('title', 'author', 'start_date', 'price')}),
        ('Доступность', {'fields': ('is_available',)}),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'course')
    list_filter = ('course',)
    search_fields = ('title', 'link')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('title', 'link', 'course')}),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'max_students')
    list_filter = ('course',)
    search_fields = ('title',)
    ordering = ('-id',)
    fieldsets = (
        (None, {'fields': ('title', 'course', 'max_students')}),
    )