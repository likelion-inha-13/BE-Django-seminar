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

def change_password(request, pk):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=pk)
        member_data = json.loads(request.body)

        if 'password' in member_data:
            member.password = member_data['password']
            member.save()

            data = {
                'password': member.password
            }
            response_data = { # 딕셔너리 형태로 response_data 생성
            'message': '비밀번호 변경 성공', # message 추가!
            'data': data, # 기존 data 도 포함
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'message': '비밀번호를 입력해주세요'}, status=400)
    else:
        return JsonResponse({'message': 'Post 요청만 허용 됩니다.'}, status=400)
    
def click_hearts(request, pk):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=pk)
        member.hearts += 1
        member.save()

        data = {
            'id': member.id,
            'name': member.name,
            'hearts': member.hearts
        }
        response_data = {
            'message': f"'{member.name}' 님에게 하트를 1개 눌렀습니다.", # f-string을 사용하여 member.name 포함
            'data': data
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'message': 'Post 요청만 허용 됩니다.'}, status=400)
    

def leader(request,pk): #필터 버전
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=pk)

        if member.is_leader:
            # 대표 자격 박탈
            member.is_leader = False
            member.save()
            message = f"'{member.name}' 님의 대표 자격을 박탈 하였습니다."
            return JsonResponse({'message': message}, status=200)
        else:
            # 대표 임명 시 기존 대표 확인 및 처리 (대표는 1명만 가능)
            existing_leader = Member.objects.filter(is_leader=True).exists()
            if existing_leader:
                return JsonResponse({'message': '대표는 2명 이상일 수 없습니다.'}, status=400)
            else:
                # 대표 임명
                member.is_leader = True
                member.save()
                message = f"'{member.name}' 님을 대표로 임명 하였습니다."
                return JsonResponse({'message': message}, status=200)

    else:
        return JsonResponse({'message': 'POST 요청만 허용됩니다.'}, status=400)
    
def leader_v2(request, pk): # 필터 안쓰는 버전
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=pk)

        if member.is_leader:
            # 대표 자격 박탈 (
            member.is_leader = False
            member.save()
            message = f"'{member.name}' 님의 대표 자격을 박탈 하였습니다."
            return JsonResponse({'message': message}, status=200)
        else:
            # 대표 임명 시 기존 대표 확인 
            members = Member.objects.all() # 모든 Member 객체 가져오기!
            leader_exists = False # 대표 존재 여부 변수
            for existing_member in members: # for 루프로 순회
                if existing_member.is_leader:
                    leader_exists = True # 대표가 존재하면 변수 True 로 변경
                    break # 대표를 찾았으면 루프 종료

            if leader_exists:
                return JsonResponse({'message': '대표는 2명 이상일 수 없습니다.'}, status=400)
            else:
                # 대표 임명 (기존 로직 동일)
                member.is_leader = True
                member.save()
                message = f"'{member.name}' 님을 대표로 임명 하였습니다."
                return JsonResponse({'message': message}, status=200)

    else:
        return JsonResponse({'message': 'POST 요청만 허용됩니다.'}, status=400)
    
def get_all_members(request):
    if request.method == 'GET':
        members = Member.objects.all()
        data = []

        for member in members:
            data.append({
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'is_leader': member.is_leader,
                'hearts': member.hearts
            })
        return JsonResponse({'posts': data}, status=200) 
    else:
        return JsonResponse({'message': 'GET 요청만 허용 됩니다.'}, status=400)
    
def delete_member(request, pk):
    if request.method == 'DELETE':
        member = get_object_or_404(Member, pk=pk)
        member.delete()
        return JsonResponse({'message': f'id: {pk} Member deleted successfully!'} ) # f-string 기능 O status=200)
    else:
        return JsonResponse({'message': 'DELETE 요청만 허용 됩니다.'}, status=400)