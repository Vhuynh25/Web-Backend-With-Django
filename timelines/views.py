
from django.http import HttpResponse, JsonResponse
from .models import Post
from django.core import serializers

import socket
import requests
import json
from datetime import datetime
import os

# Create your views here.


def index(request):
    return HttpResponse("Hello")


def public(request):
    posts = []
    try:
        posts.append(list(Post.objects.order_by('-timestamp').values()))
    except Exception:
        response = HttpResponse()
        response.status_code = 404
        return response
    return HttpResponse(posts)


def timeline(request, user):
    posts = []

    try:
        id_user = Post.objects.filter(username=user).values('user_id')[0]['user_id']

        # finds all user's existing posts
        posts.append(list(Post.object.get(user_id=id_user)))

    except Exception:
        response = HttpResponse()
        response.status_code = 404
        return response
    return HttpResponse(posts)


def get_post(request, user, post_id):
    response = HttpResponse()
    posts = []
    try:
        id_user = Post.objects.filter(username=user).values('user_id')[0]['user_id']

        # finds user's specific post
        posts.append(list(Post.object.get(user_id=id_user, id=post_id)))

    except Exception:
        response = HttpResponse()
        response.status_code = 404
        return response
    return HttpResponse(posts)


def create_post(request, user):
    response = HttpResponse()
    body = json.loads(request.body)
    try:

        # set timestamp
        now = datetime.now()
        date_time = now.strftime("%Y/%m/%d %H:%M:%S")
        id_user = Post.objects.filter(username=user).values('user_id').first()
        p = Post(
            text=body['text'],
            user_id=id_user,
            username=user,
            timestamp=date_time
        )
        if not "url" in body:
            p.url = ""
        else:
            p.url = body["url"]
        p.save()

    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 409
        return response

    response.header["Location"] = f"/timeline/{user}/{p.id}"
    return JsonResponse(p, safe=False)


def check_health(request):
    try:
        posts = [list(Post.objects.order_by('-timestamp').values())]
        return HttpResponse(posts)
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 409
        return response


def self_register(api):
    registerurl = "http://localhost:8000/registry/timelines"
    url = "http://" + socket.gethostbyname(socket.gethostname()) + ":" + os.environ["PORT"] + "/timelines"
    r = requests.post(registerurl, data={"text": url})
