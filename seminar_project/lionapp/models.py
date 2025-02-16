from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100) # 100글자가 최대인 문자열
    content = models.TextField() # 글자 수 제한이 없는 긴 문자열
    create_at = models.DateTimeField(auto_now_add=True) # 처음 Post 생성시, 현재시간 저장


class Comment(models.Model):
    content = models.CharField(max_length = 200, null = True, blank = True) # 100글자가 최대인 문자열, empty값을 null로 저장 
    post_id = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE, related_name="comments") # Post와 일대다 관계설정, Post삭제시 Comment도 삭제, 역참조 설정

    def __str__(self):
        return self.content #str_method를 통해 각 객체 구분 