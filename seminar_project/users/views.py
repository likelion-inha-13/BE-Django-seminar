from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny]) # 회원가입 api는 누구나 접근 가능
def signup(request):
    # email = request.data.get('email')
    # password = request.data.get('password')
    # name = request.data.get('name')

    serializer = UserSerializer(data=request.data)
    # 시리얼라이저를 통해 위 주석코드를 한번에 처리

    if serializer.is_valid(raise_exception=True): # 유효성 검사
        user = serializer.save()
        user.set_password(request.data['password']) # 비밀번호 해싱
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny]) # 로그인 api도 누구나 접근 가능
# 로그인을 통해 JWT 토큰 발급
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password) # 사용자 인증
    if user is None:
        return Response({'message': '아이디 또는 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user) # JWT Refresh Token 생성
    update_last_login(None, user) # 마지막 로그인 시간 업데이트

    return Response({'refresh_token': str(refresh),
                     'access_token': str(refresh.access_token), }, status=status.HTTP_200_OK)

    # refresh.access_token -> Access Token 자동 생성
    # str로 토큰을 변환해주는 이유 : RefreshToken 객체는 JSON으로 변환할 수 없어서 문자열로 변환을 해줘야 JSON으로 반환가능함!