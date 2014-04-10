import json
from django.http import HttpResponse
from interface.requests import functionsDB

def create(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        params = {}
        for a in ["isDeleted"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            for a in dataRequired:
                if a not in dataRequest:
                    raise Exception("no element " + a)
                if dataRequest[a] is not None:
                    try:
                        dataRequest[a] = dataRequest[a].encode('utf-8')
                    except Exception:
                        continue
            thread = functionsDB.saveThread(forum=dataRequest["forum"], title=dataRequest["title"], isClosed=dataRequest["isClosed"],
                                     user=dataRequest["user"], date=dataRequest["date"], message=dataRequest["message"],
                                     slug=dataRequest["slug"], optional=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def details(request):
    if request.method == "GET":
        dataRequest = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["thread"]
        try:
            related = dataRequest["related"]
        except KeyError:
            related = []
        try:
            thread = functionsDB.detailsThread(id=dataRequest["thread"], related=related)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def vote(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread", "vote"]
        try:
            thread = functionsDB.voteThread(id=dataRequest["thread"], vote=dataRequest["vote"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def subscribe(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread", "user"]
        try:
            subscription = functionsDB.saveSubscription(email=dataRequest["user"], thread_id=dataRequest["thread"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": subscription}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)



def unsubscribe(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread", "user"]
        try:
            subscription = functionsDB.removeSubscription(email=dataRequest["user"], thread_id=dataRequest["thread"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": subscription}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def open(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread"]
        try:
            thread = functionsDB.openCloseThread(id=dataRequest["thread"], isClosed=0)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def close(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread"]
        try:
            thread = functionsDB.openCloseThread(id=dataRequest["thread"], isClosed=1)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def update(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread", "slug", "message"]
        try:
            thread = functionsDB.updateThread(id=dataRequest["thread"], slug=dataRequest["slug"], message=dataRequest["message"])
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def remove(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread"]
        try:
            thread = functionsDB.removeRestoreThread(thread_id=dataRequest["thread"], status=1)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def restore(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        dataRequired = ["thread"]
        try:
            thread = functionsDB.removeRestoreThread(thread_id=dataRequest["thread"], status=0)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": thread}
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
                identif = dataRequest["user"]
                entity = "user"
            except KeyError:
                dataResponse = {"code": 1, "response": "forum or thread no"}
                return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        for a in ["limit", "order", "since"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            treadsList = functionsDB.listThread(entity=entity, identificator=identif, related=[], params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": treadsList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)


def listPosts(request):
    if request.method == "GET":
        dataRequest = {}
        params = {}
        for a in request.GET:
            dataRequest[a] = request.GET.get(a)
        dataRequired = ["thread"]
        entity = "thread"
        for a in ["limit", "order", "since"]:
            try:
                params[a] = dataRequest[a]
            except KeyError:
                continue
        try:
            postsList = functionsDB.listPost(entity=entity, identificator=dataRequest["thread"], related=[], params=params)
        except Exception as e:
            dataResponse = {"code": 1, "response": e.message}
            return HttpResponse(json.dumps(dataResponse), content_type='application/json')
        dataResponse = {"code": 0, "response": postsList}
        return HttpResponse(json.dumps(dataResponse), content_type='application/json')
    else:
        return HttpResponse(status = 400)