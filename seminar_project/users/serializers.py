from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # 비밀번호는 함부로 수정이 불가능

    class Meta:
        model = get_user_model() # 현재 사용 주인 User 모델 가져옴
        fields = ('id', 'user_id', 'email', 'password', 'name', 'generation', 'gender')


# 패스워드가 필요없는 다른 테이블에서 사용할 용도
# 즉, 패스워드 없는 유저 정보
class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'user_id', 'email', 'name', 'generation', 'gender')