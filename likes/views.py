from django.shortcuts import render
from django.http import HttpResponse
from timelines.models import Post

import requests
import socket
import os
import json


import redis
import greenstalk
# Create your views here.

red = redis.Redis(host='localhost', port=6379, db=0)
red.flushall()  # Deletes db when ran

msq_queue = greenstalk.Client(('127.0.0.1', 11300),watch="likes")


def fill_db():
    for x in Post.objects.values():
        username = x["username"]
        post_id = x["post_id"]
        url = "/likes/" + username + "/" + str(post_id)
        red.zadd("post_list", {url: 0})


fill_db()


def like(request, liker_username, username, post_id):
    url = "/likes/" + username + "/" + post_id
    try:
        red.zincrby("post_list", 1, url) # increment post_list by 1
        red.sadd(liker_username, url)
        red.zincrby("popular_list", 1, url)
        call_post_check(post_id,username,liker_username)
    except Exception:
        response = HttpResponse()
        response.status_code = 404
        return response
    response = HttpResponse()
    response.status_code = 202
    return response


def like_counts(username, post_id):
    url = "/likes/" + username + "/" + post_id
    output = red.zscore("post_list", url)
    return {"url": url, "total likes": output}


def user_liked(liker_username):
    output = red.smembers(liker_username)
    return {"User Likes": output}


def popular_post(request):
    output = red.zrevrange("popular_list", 0, -1, withscores=True)
    return {"Popular Posts": output}


def check_health(request):
    try:
        return red.ping()
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 404
        return response


def self_register(api):
    registerurl = "http://localhost:8000/registry/likes"
    url = "http://" + socket.gethostbyname(socket.gethostname()) + ":" + os.environ["PORT"] + "/likes"
    r = requests.post(registerurl, data={"text": url})


def call_post_check(post_id,username,liker_username):
    msq_queue.use("likes")
    body = json.dumps({
        "post_id": post_id,
        "username": username,
        "liker_username": liker_username
    })
    msq_queue.put(body)
    return
