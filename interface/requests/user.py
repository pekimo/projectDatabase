import json
from django.http import HttpResponse
from interface.requests import functionsDB

def create(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["email", "username", "name", "about"]
        params = {}
        for a in ["isAnonymous"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            user = functionsDB.saveUser(email=dataRequest["email"], username=dataRequest["username"],
                               about=dataRequest["about"], name=dataRequest["name"], optional=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": user}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def details(request):
    if request.method == "GET":
        dataRequest = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["user"]
        try:
            userDetails = functionsDB.detailsUser(email=dataRequest["user"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": userDetails}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def follow(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["follower", "followee"]
        try:
            following = functionsDB.addFollower(email1=dataRequest["follower"], email2=dataRequest["followee"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": following}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def unfollow(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["follower", "followee"]
        try:
            following = functionsDB.removeFollower(email1=dataRequest["follower"], email2=dataRequest["followee"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": following}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def listFollowers(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["user"]
        for a in ["limit", "order", "since_id"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            followerList = functionsDB.listFollower(email=dataRequest["user"], type="follower", params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": followerList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def listFollowing(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["user"]
        for a in ["limit", "order", "since_id"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            followings = functionsDB.listFollower(email=dataRequest["user"], type="followee", params=dataRequest)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": followings}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def listPosts(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["user"]
        for a in ["limit", "order", "since"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            postsList = functionsDB.listPost(entity="user", identificator=dataRequest["user"], related=[], params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": postsList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def updateProfile(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["user", "name", "about"]
        try:
            user = functionsDB.updateUser(email=dataRequest["user"], name=dataRequest["name"], about=dataRequest["about"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": user}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)