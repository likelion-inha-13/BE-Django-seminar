import json  
from django.http import JsonResponse  
from .models import *  


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
