from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    class Meta:
        model = Post
        fields = ["id","title","content"]
        # Post 모델의 모든 필드에 대해서 직렬화 하고 싶은 경우는 아래와 같이 작성
        # fields = '__all__'