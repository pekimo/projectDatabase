import json
from django.http import HttpResponse
from interface.requests import functionsDB

def create(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["name", "short_name", "user"]
        try:
            for a in dataRequired:
                if a not in dataRequest:
                    raise Exception("no element " + a)
                if dataRequest[a] is not None:
                    try:
                        dataRequest[a] = dataRequest[a].encode('utf-8')
                    except Exception:
                        continue
            forum = functionsDB.saveForum(name=dataRequest["name"], short_name=dataRequest["short_name"], user=dataRequest["user"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": forum}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')    
    else:
        return HttpResponse(status = 400)


def details(request):
    if request.method == "GET":
        dataRequest = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["forum"]
        try:
            related = dataRequest["related"]
        except KeyError:
            related = []
        try:
            forum = functionsDB.detailsForum(short_name=dataRequest["forum"], related=related)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": forum}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def listPosts(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["forum"]
        try:
            related = dataRequest["related"]
        except KeyError:
            related = []
        for a in ["limit", "order", "since"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            postsList = functionsDB.listPost(entity="forum", identificator=dataRequest["forum"],
                                       related=related, params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": postsList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def listThreads(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["forum"]
        try:
            related = dataRequest["related"]
        except KeyError:
            related = []
        for a in ["limit", "order", "since"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            threadsList = functionsDB.listThread(entity="forum", identificator=dataRequest["forum"],
                                             related=related, params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": threadsList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)

def listUsers(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["forum"]
        for a in ["limit", "order", "since_id"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            usersList = functionsDB.listUsersForum(dataRequest["forum"], params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": usersList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)