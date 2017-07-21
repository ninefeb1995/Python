from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'updated')
    list_display_links = ('updated',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_editable = ('title',)
    class Meta:
        model = Post


# Register your models here.
admin.site.register(Post, PostAdmin)