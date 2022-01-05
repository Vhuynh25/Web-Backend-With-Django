from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import User, Follow
# Create your views here.

import json

import pdb


def get_users(request):
    users = []

    try:
        users.append(list(User.objects.values()))
    except Exception:
        response = HttpResponse()
        response.status_code = 404
        return response

    return HttpResponse(users)


def user_request(request, username):

    if request.method == 'GET':
        return get_user(username)
    elif request.method == 'POST':
        return add_user(request, username)
    else:
        response = HttpResponse()
        response.status_code = 404
        return response


def get_user(user):
    users = []
    try:
        users.append(list(User.objects.filter(username=user).values().first()))

    except Exception:

        response = HttpResponse()
        response.status_code = 404
        return response

    return HttpResponse(users)


def get_follows(request, user):

    follows = []

    try:
        follows.append(list(Follow.objects.filter(username=user).values("followed_name")))

    except Exception:
        response = HttpResponse()
        response.status_code = 404
        return response
    return HttpResponse(follows)


def check_health(request):
    pdb.set_trace()
    try:
        users = [list(User.objects.values())]
        return HttpResponse(users)
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 404
        return response


# http localhost:8000/users/brandon2306 email="brand@testmail.com" bio="testing testing" password="testpass123"
def add_user(request, user):
    body = json.loads(request.body)
    try:
        ur = User(
            bio=body['bio'],
            email=body['email'],
            username=user,
            password=body['password']
        )
        ur.save()

    except Exception as e:

        response = HttpResponse(str(e))
        response.status_code = 409
        return response
    response = HttpResponse()
    response.status_code = 202
    #response.header["Location"] = f"/users/{user}/{ur.id}"
    return response


def get_password(request, user_id, password):
    if password == User.objects.filter(id=user_id).values('password').first():
        response = HttpResponse()
        response.status_code = 200
        return response
    else:
        response = HttpResponse("Passwords do not match")
        response.status_code = 409
        return response


