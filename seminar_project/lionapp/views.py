import json  
from django.http import JsonResponse  
from .models import *  
from django.shortcuts import get_object_or_404

def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        title = data.get('title')
        content = data.get('content')

        post = Post(
            title = title,
            content = content
        )
        post.save()
        return JsonResponse({'message':'success'})
    return JsonResponse({'message':'POST 요청만 허용됩니다.'})


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
	else:  
		return JsonResponse({'message':'GET 요청만 허용됩니다.'})  # 에러 메시지를 JSON 형식으로 응답
	


def get_posts_all(request): 
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
    else: 
        return JsonResponse({'message': 'GET 요청만 허용됩니다.'}) 