from django.shortcuts import render

from django.http import HttpResponse


def health(request):
    return HttpResponse(status = 200, content = "seminar server ok!")