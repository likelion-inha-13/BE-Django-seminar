from django.contrib import admin

from .models import Post

# Register your models here.
admin.site.register(Post) # Post 모델을 admin 페이지에서 관리할 수 있도록 등록