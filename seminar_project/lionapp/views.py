import json  
from django.http import JsonResponse  
from .models import *  
from django.shortcuts import get_object_or_404 # 추가하기 객체가 없으면 404 오류를 발생시키는 함수

def create_member(request):  
    if request.method == 'POST':  
        member_data = json.loads(request.body)  
        
        name = member_data['name']
        email = member_data['email']
        is_leader = member_data['is_leader']
        hearts = member_data['hearts']

        member = Member(
            name=name,
            email=email,
            is_leader=is_leader,
            hearts=hearts
        )
        member.save()
        return JsonResponse({'message': 'Member created successfully!'}, status=200)
    return JsonResponse({'message': 'Post 요청만 허용 됩니다.'}, status=400)


def get_members(request,pk):
    if request.method == 'GET':
        member = get_object_or_404(Member, pk=pk)
        data = { 
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "is_leader": member.is_leader,
            "hearts": member.hearts
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'message': 'GET 요청만 허용 됩니다.'}, status=400)
