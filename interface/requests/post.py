import json
from django.http import HttpResponse
from interface.requests import functionsDB

def create(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["user", "forum", "thread", "message", "date"]
        params = {}
        for a in ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue 
        try:
            post = functionsDB.createPost(date=dataRequest["date"], thread=dataRequest["thread"],
                                message=dataRequest["message"], user=dataRequest["user"],
                                forum=dataRequest["forum"], optional=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": post}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def details(request):
    if request.method == "GET":
        dataRequest = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["post"]
        try:
            related = dataRequest["related"]
        except KeyError:
            related = []
        try:
            post = functionsDB.detailsPost(dataRequest["post"], related=related)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": post}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def list(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        identif = None
        try:
            identif = dataRequest["forum"]
            entity = "forum"
        except KeyError:
            try:
                identif = dataRequest["thread"]
                entity = "thread"
            except KeyError:
                dataResponse = {"code": 1, "response": "forum or thread no"}
                return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        for a in ["limit", "order", "since"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            postsList = functionsDB.listPost(entity=entity, identificator=identif, related=[], params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": postsList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def remove(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["post"]
        try:
            post = functionsDB.removeRestorePost(post_id=dataRequest["post"], status=1)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": post}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def restore(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["post"]
        try:
            post = functionsDB.removeRestorePost(post_id=dataRequest["post"], status=0)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": post}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def update(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["post", "message"]
        try:
            post = functionsDB.updatePost(id=dataRequest["post"], message=dataRequest["message"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": post}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def vote(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["post", "vote"]
        try:
            post = functionsDB.votePost(id=dataRequest["post"], vote=dataRequest["vote"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": post}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)