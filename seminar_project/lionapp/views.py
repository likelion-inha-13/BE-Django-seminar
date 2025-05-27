import json  
from django.http import JsonResponse  
from .models import *  
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@api_view(['POST'])
def create_post(request): # drf 기능 추가된 함수
    title = request.data.get('title')  # request.body 대신 request.data 사용
    content = request.data.get('content')

    if not title or not content:
        return Response({'message': '제목과 내용을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    post = Post.objects.create(title=title, content=content)
    
    return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
    # JsonResponse 대신 Response 사용

@swagger_auto_schema(
    method="post",
    request_body=PostSerializer,
    operation_summary="Post 생성 API",
    operation_description="제목과 내용을 입력받아 Post를 생성합니다.",
    responses={
        201: "생성 성공",
        400: "잘못된 요청",
    },
    tags=["Post"]
)
@api_view(['POST'])
def create_post_v2(request):
    serializer = PostSerializer(data=request.data) # JSON → Python 객체 변환 (역직렬화)
    
    if serializer.is_valid():  # 데이터 유효성 검사
        post = serializer.save()  # DB 저장
        message = f"id: {post.pk}번 포스트 생성 성공"
        return Response({'message': message, 'post': serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 유효성 검사 실패 시 오류 반환


@swagger_auto_schema(
    method='get',
    operation_summary="Post 단일 조회 (FBV)",
    operation_description="pk 값으로 특정 게시글을 조회합니다.",
    responses={200: "조회 성공", 404: "게시글 없음"},
    tags=["Post"]
)
@api_view(['GET'])
def get_post(request, pk):  # 특정 Post 객체를 조회하는 함수
	if request.method == 'GET':  # HTTP 요청 메서드가 GET인지 확인
		post = get_object_or_404(Post, pk=pk)  # Post 모델에서 pk에 해당하는 객체를 가져옴, 없으면 404 오류 발생
		data = {  # 응답으로 보낼 데이터를 딕셔너리 형태로 구성
			'id': post.pk,  # Post 객체의 ID
			'제목': post.title,  # Post 객체의 제목
			'내용': post.content,  # Post 객체의 내용
			'메시지': '조회 성공'  
		}
		return JsonResponse(data, status=200) 
	return JsonResponse({'message':'GET 요청만 허용됩니다.'})  # 에러 메시지를 JSON 형식으로 응답
	

@swagger_auto_schema(
    method='get',
    operation_summary="모든 Post 조회",
    operation_description="전체 게시글을 리스트로 조회합니다.",
    responses={200: "조회 성공"},
    tags=["Post"]
)
@api_view(['GET'])
def get_post_all(request): 
    if request.method == 'GET': # GET 요청으로만 동작하도록 제한
        posts = Post.objects.all()  # all() 메서드로 모든 Post 객체 조회 
        data = []  # 응답으로 보낼 데이터를 담을 리스트 초기화

        for post in posts: # 각 Post 객체 정보 추출
            data.append({ # 추출된 정보 ->  data 리스트에 추가
                'id': post.id,
                '제목': post.title, 
                '내용': post.content,
                '메시지': '조회 성공' # "메시지" 필드 추가
            })
        return JsonResponse({'posts': data}, status=200) 
    return JsonResponse({'message': 'GET 요청만 허용됩니다.'}) 

@swagger_auto_schema(
    method='post',
    request_body=PostSerializer,
    operation_summary="Post 수정 (FBV)",
    operation_description="pk에 해당하는 게시글을 수정합니다.",
    responses={200: "수정 성공", 400: "잘못된 요청"},
    tags=["Post"]
)
@api_view(['POST'])
def update_post(request, pk):
    if request.method == 'POST':  
        post = get_object_or_404(Post, pk=pk)  # Post 모델에서 pk에 해당하는 객체를 가져옴, 없으면 404 오류 발생
        data = json.loads(request.body)  

        if 'title' in data:  # 요청 데이터에 'title' 내용이 있는지 확인
            post.title = data['title']  # Post 객체의 'title' 필드를 요청 데이터의 값으로 업데이트
        if 'content' in data:  # 요청 데이터에 'content' 내용이 있는지 확인
            post.content = data['content']  # Post 객체의 'content' 필드를 요청 데이터의 값으로 업데이트

        post.save()  # 변경된 Post 객체를 데이터베이스에 저장

        data = {  # 수정 성공 시 응답으로 보낼 데이터를 딕셔너리 형태로 구성
            'post': {  # 수정된 게시글 정보
                'id': post.id,  
                '제목': post.title, 
                '내용': post.content, 
            },
            'message': f'id: {pk}번 게시글 수정 성공' 
        }
        return JsonResponse(data, status=200)  
    return JsonResponse({'message': 'POST 요청만 허용됩니다.'}, status=400)  

@swagger_auto_schema(
    method='delete',
    operation_summary="Post 삭제 (FBV)",
    operation_description="pk에 해당하는 게시글을 삭제합니다.",
    responses={200: "삭제 성공", 404: "게시글 없음"},
    tags=["Post"]
)
@api_view(['DELETE'])
def delete_post(request, pk):
    if request.method == 'DELETE':
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        data = {
            "message" : f"id: {pk} 포스트 삭제 완료"
        }
        return JsonResponse(data, status=200)
    return JsonResponse({'message':'DELETE 요청만 허용됩니다.'})


class PostApiView(APIView) : # CBV로 get_post, delete_post 리팩토링
    
    @swagger_auto_schema(
        operation_summary="Post 단일 조회",
        operation_description="pk에 해당하는 게시글을 조회합니다.",
        responses={200: "조회 성공", 404: "게시글 없음"},
        tags=["Post"]
    )
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        postSerializer = PostSerializer(post) # Python -> JSON 변환 (직렬화)
        message = f"id: {post.pk}번 포스트 조회 성공"
        return Response({'message': message, 'post': postSerializer.data}, status=status.HTTP__200_OK)
    
    @swagger_auto_schema(
        operation_summary="Post 삭제",
        operation_description="pk에 해당하는 게시글을 삭제합니다.",
        responses={200: "삭제 성공", 404: "게시글 없음"},
        tags=["Post"]
    )
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        
        message = f"id: {pk}번 포스트 삭제 성공"
        return Response({'message': message}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=PostSerializer,
        operation_summary="Post 수정",
        operation_description="pk에 해당하는 게시글을 일부 수정합니다.",
        responses={200: "수정 성공", 400: "유효성 실패", 404: "게시글 없음"},
        tags=["Post"]
    )
    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)  # 부분 업데이트 허용

        if serializer.is_valid():
            serializer.save()
            message = f"id: {pk}번 포스트 업데이트 성공"
            return Response({'message': message, 'post': serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


