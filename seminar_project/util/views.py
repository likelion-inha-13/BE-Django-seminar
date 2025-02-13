from django.shortcuts import render

from django.http import HttpResponse  


def health(request):               
    # 웹 브라우저에서 요청이 들어오면 이 함수가 실행됩니다.
    # 'request'는 웹 브라우저에서 보낸 요청에 대한 정보가 들어있어요.
    return HttpResponse("seminar server ok!")  # 웹 페이지에 "seminar server ok!" 라는 글자를 보여줘요!
    # HttpResponse는 웹 페이지에 글자나 그림을 보여줄 때 사용하는 도구입니다.