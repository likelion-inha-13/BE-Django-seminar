from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100) # 100글자가 최대인 문자열
    content = models.TextField() # 글자 수 제한이 없는 긴 문자열
    create_at = models.DateTimeField(auto_now_add=True) # 처음 Post 생성시, 현재시간 저장