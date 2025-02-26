from django.db import models

# Create your models here.
class member(models.Model):
    name = models.CharField(max_length=100) # 이름을 저장하는 필드
    email = models.EmailField() # 이메일을 저장하는 필드
    is_leader = models.BooleanField(default=False) # 리더 여부를 저장하는 필드
    hearts = models.IntegerField(default=0) # 하트 개수를 저장하는 필드