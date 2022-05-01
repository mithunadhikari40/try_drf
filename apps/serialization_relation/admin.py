from django.contrib import admin
from .models import Singer, Song


# Register the model classes in admin, one way of doing it
# @admin.register(Singer)
# class SingerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'gender']

# Register the model classes in admin

class SingerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender']


admin.site.register(Singer, SingerAdmin)


class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'singer', 'duration']


admin.site.register(Song, SongAdmin)
