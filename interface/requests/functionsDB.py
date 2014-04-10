from interface.requests import ConnectionDB
from interface.requests.ConnectionDB import ConnectionDataBase

#-----------------------------------------------------------

def saveForum(name, short_name, user):
    ConnectionDB.exist(entity="Users", identificator="email", value=user)
    forum = ConnectionDB.funQuery('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name,))
    if len(forum) == 0:
        ConnectionDB.funUpdate('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)',(name, short_name, user,))
        forum = ConnectionDB.funQuery('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    return descriptionForum(forum)


def descriptionForum(forum):
    forum = forum[0]
    response = {'id': forum[0],'name': forum[1],'short_name': forum[2],'user': forum[3]}
    return response


def detailsForum(short_name, related):
    forum = ConnectionDB.funQuery('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name,))
    if len(forum) == 0:
        raise ("No forum with " + short_name)
    forum = descriptionForum(forum)
    if "user" in related:
        forum["user"] = detailsUser(forum["user"])
    return forum


def listUsersForum(short_name, optional):
    ConnectionDB.exist(entity="Forums", identificator="short_name", value=short_name)
    query = "SELECT DISTINCT email FROM Users JOIN Posts ON Posts.user = Users.email "" JOIN Forums on Forums.short_name = Posts.forum WHERE Posts.forum = %s "
    if "since_id" in optional:
        query += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY Users.id " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])
    users_ = ConnectionDB.funQuery(query, (short_name,))
    listU = []
    for user in users_:
        user = user[0]
        listU.append(detailsUser(user))
    return listU

#------------------------------------------------------------------------------------------------

def createPost(date, thread, message, user, forum, optional):
    ConnectionDB.exist(entity="Threads", identificator="id", value=thread)
    ConnectionDB.exist(entity="Forums", identificator="short_name", value=forum)
    ConnectionDB.exist(entity="Users", identificator="email", value=user)
    if len(ConnectionDB.funQuery("SELECT Threads.id FROM Threads JOIN Forums ON Threads.forum = Forums.short_name "
                                "WHERE Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("no thread with id = " + thread + " in forum " + forum)
    if "parent" in optional:
        if len(ConnectionDB.funQuery("SELECT Posts.id FROM Posts JOIN Threads ON Threads.id = Posts.thread "
                             "WHERE Posts.id = %s AND Threads.id = %s", (optional["parent"], thread, ))) == 0:
            raise Exception("No post with id = " + optional["parent"])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]

    for param in optional:
        query += ", "+param
        values += ", %s"
        parameters.append(optional[param])

    query += ") VALUES " + values + ")"

    update_thread_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"

    connection = ConnectionDataBase()
    connection = connection.connect()
    connection.autocommit(False)
    with connection:
        cursor = connection.cursor()
        try:
            connection.begin()
            cursor.execute(update_thread_posts, (thread, ))
            cursor.execute(query, parameters)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception("Database error: " + e.message)
        post_id = cursor.lastrowid
        cursor.close()
    connection.close()
    post = queryPost(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def detailsPost(id, related):
    post = queryPost(id)
    if post is None:
        raise Exception("no post with id = "+id)
    if "user" in related:
        post["user"] = detailsUser(post["user"])
    if "forum" in related:
        post["forum"] = detailsForum(short_name=post["forum"], related=[])
    if "thread" in related:
        post["thread"] = detailsThread(id=post["thread"], related=[])

    return post


def listPost(entity, identificator, related, params):
    if entity == "forum":
        ConnectionDB.exist(entity="Forums", identificator="short_name", value=identificator)
    if entity == "thread":
        ConnectionDB.exist(entity="Threads", identificator="id", value=identificator)
    if entity == "user":
        ConnectionDB.exist(entity="Users", identificator="email", value=identificator)
    query = "SELECT id FROM Posts WHERE " + entity + " = %s "
    parameters = [identificator]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    post_ids = ConnectionDB.funQuery(query=query, params=parameters)
    postList = []
    for id in post_ids:
        id = id[0]
        postList.append(detailsPost(id=id, related=related))
    return postList


def removeRestorePost(post_id, status):
    ConnectionDB.exist(entity="Posts", identificator="id", value=post_id)
    ConnectionDB.funUpdate("UPDATE Posts SET isDeleted = %s WHERE Posts.id = %s", (status, post_id, ))
    return {
        "post": post_id
    }


def updatePost(id, message):
    ConnectionDB.exist(entity="Posts", identificator="id", value=id)
    ConnectionDB.funUpdate('UPDATE Posts SET message = %s WHERE id = %s', (message, id, ))
    return detailsPost(id=id, related=[])


def votePost(id, vote):
    ConnectionDB.exist(entity="Posts", identificator="id", value=id)
    if vote == -1:
        ConnectionDB.funUpdate("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        ConnectionDB.funUpdate("UPDATE Posts SET likes=likes+1, points=points+1  where id = %s", (id, ))
    return detailsPost(id=id, related=[])

def selectPost(query, params):
    return ConnectionDB.funQuery(query, params)

def queryPost(id):
    post = selectPost('select date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM Posts WHERE id = %s', (id, ))
    if len(post) == 0:
        return None
    return describePost(post)


def describePost(post):
    post = post[0]
    postResponse = {'date': str(post[0]), 'dislikes': post[1], 'forum': post[2], 'id': post[3], 'isApproved': bool(post[4]),
        			'isDeleted': bool(post[5]), 'isEdited': bool(post[6]), 'isHighlighted': bool(post[7]), 'isSpam': bool(post[8]),
        			'likes': post[9], 'message': post[10], 'parent': post[11], 'points': post[12], 'thread': post[13], 'user': post[14],
    }
    return postResponse

#-----------------------------------------------------------------------------------------------------------------------    

def saveUser(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        user = selectUser('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
        if len(user) == 0:
            ConnectionDB.funUpdate('INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',(email, about, name, username, isAnonymous,))
        user = selectUser('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',(email,))
    except Exception as e:
        raise Exception(e.message)
    return describeUser(user)


def updateUser(email, about, name):
    ConnectionDB.exist(entity="Users", identificator="email", value=email)
    ConnectionDB.funUpdate('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',(email, about, name, email,))
    return detailsUser(email)

def followersUser(email, type):
    temp = "followee"
    if type == "follower":
        temp = "followee"
    if type == "followee":
        temp = "follower"
    listF = ConnectionDB.funQuery("SELECT "+type+" FROM Followers JOIN Users ON Users.email = Followers." +type+" WHERE "+temp+" = %s ", (email, )
    )
    return tuple(listF)

def detailsUser(email):
    user = queryUser(email)
    if user is None:
        raise Exception("No user with email " + email)
    user["followers"] = followersUser(email, "follower")
    user["following"] = followersUser(email, "followee")
    user["subscriptions"] = subscriptionsUser(email)
    return user

def subscriptionsUser(email):
    listS = []
    subscriptions = ConnectionDB.funQuery('SELECT thread FROM Subscriptions WHERE user = %s', (email,))
    for a in subscriptions:
        listS.append(a[0])
    return listS

def queryUser(email):
    user = selectUser('SELECT email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email,))
    if len(user) == 0:
        return None
    return describeUser(user)

def describeUser(user):
    user = user[0]
    userResponse = { 'about': user[1], 'email': user[0], 'id': user[3], 'isAnonymous': bool(user[2]), 'name': user[4], 'username': user[5] }
    return userResponse

def selectUser(query, params):
    return ConnectionDB.funQuery(query, params)

def tuple(list):
    newList = []
    for el in list:
        newList.append(el[0])
    return newList

#---------------------------------------------------------------------------------------------------------    

def saveThread(forum, title, isClosed, user, date, message, slug, optional):
    ConnectionDB.exist(entity="Users", identificator="email", value=user)
    ConnectionDB.exist(entity="Forums", identificator="short_name", value=forum)
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    thread = ConnectionDB.funQuery('select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM Threads WHERE slug = %s', (slug,))
    if len(thread) == 0:
        ConnectionDB.funUpdate('INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(forum, title, isClosed, user, date, message, slug, isDeleted,))
        thread = ConnectionDB.funQuery('select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM Threads WHERE slug = %s', (slug,))
    response = descriptionThread(thread)
    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]
    return response


def detailsThread(id, related):
    thread = ConnectionDB.funQuery('SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM Threads WHERE id = %s', (id,))
    if len(thread) == 0:
        raise Exception('No thread id =' + str(id))
    thread = descriptionThread(thread)
    if "user" in related:
        thread["user"] = detailsUser(thread["user"])
    if "forum" in related:
        thread["forum"] = detailsForum(short_name=thread["forum"], related=[])
    return thread


def descriptionThread(thread):
    thread = thread[0]
    response = {'date': str(thread[0]), 'forum': thread[1], 'id': thread[2], 'isClosed': bool(thread[3]), 'isDeleted': bool(thread[4]),
                'message': thread[5], 'slug': thread[6], 'title': thread[7], 'user': thread[8], 'dislikes': thread[9], 'likes': thread[10],
                'points': thread[11], 'posts': thread[12],
    }
    return response


def voteThread(id, vote):
    ConnectionDB.exist(entity="Threads", identificator="id", value=id)
    if vote == -1:
        ConnectionDB.funUpdate("UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s", (id,))
    else:
        ConnectionDB.funUpdate("UPDATE Threads SET likes=likes+1, points=points+1  where id = %s", (id,))
    return detailsThread(id=id, related=[])


def openCloseThread(id, isClosed):
    ConnectionDB.exist(entity="Threads", identificator="id", value=id)
    ConnectionDB.funUpdate("UPDATE Threads SET isClosed = %s WHERE id = %s", (isClosed, id, ))
    response = {
        "thread": id
    }
    return response


def updateThread(id, slug, message):
    ConnectionDB.exist(entity="Threads", identificator="id", value=id)
    ConnectionDB.funUpdate('UPDATE Threads SET slug = %s, message = %s WHERE id = %s', (slug, message, id,))
    return detailsThread(id=id, related=[])


def listThread(entity, identificator, related, params):
    if entity == "forum":
        ConnectionDB.exist(entity="Forums", identificator="short_name", value=identificator)
    if entity == "user":
        ConnectionDB.exist(entity="Users", identificator="email", value=identificator)
    query = "SELECT id FROM Threads WHERE " + entity + " = %s "
    parameters = [identificator]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    thread = ConnectionDB.funQuery(query=query, params=parameters)
    threadL = []
    for id in thread:
        id = id[0]
        threadL.append(detailsThread(id=id, related=related))
    return threadL


def removeRestoreThread(thread_id, status):
    ConnectionDB.exist(entity="Threads", identificator="id", value=thread_id)
    ConnectionDB.funUpdate("UPDATE Threads SET isDeleted = %s WHERE id = %s", (status, thread_id,))
    response = {
        "thread": thread_id
    }
    return response

#------------------------------------------------------------------------------------------------------------------------

def addFollower(email1, email2):
    ConnectionDB.exist(entity="Users", identificator="email", value=email1)
    ConnectionDB.exist(entity="Users", identificator="email", value=email2)
    if email1 == email2:
        raise Exception(email1 + "can't follow")
    follows = ConnectionDB.funQuery('SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2,))
    if len(follows) == 0:
        ConnectionDB.funUpdate('INSERT INTO Followers (follower, followee) VALUES (%s, %s)',(email1, email2, ))
    user = detailsUser(email1)
    return user

def listFollower(email, type, params):
    ConnectionDB.exist(entity="Users", identificator="email", value=email)
    if type == "follower":
        temp = "followee"
    if type == "followee":
        temp = "follower"
    query = "SELECT "+type+" FROM Followers JOIN Users ON Users.email = Followers."+type+" WHERE "+temp+" = %s "
    if "since_id" in params:
        query += " AND Users.id >= "+str(params["since_id"])
    if "order" in params:
        query += " ORDER BY Users.name "+params["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in params:
        query += " LIMIT "+str(params["limit"])
    followers = ConnectionDB.funQuery(query=query, params=(email,))
    listF = []
    for id in followers:
        id = id[0]
        listF.append(detailsUser(email=id))
    return listF


def removeFollower(email1, email2):
    follows = ConnectionDB.funQuery('SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2,))
    if len(follows) != 0:
        ConnectionDB.funUpdate('DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2,))
    else:
        raise Exception("No following")
    return detailsUser(email1)    

#----------------------------------------------------------------------------------------------------------------------------

def saveSubscription(email, thread_id):
    ConnectionDB.exist(entity="Threads", identificator="id", value=thread_id)
    ConnectionDB.exist(entity="Users", identificator="email", value=email)
    subscription = ConnectionDB.funQuery('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id,))
    if len(subscription) == 0:
        ConnectionDB.funUpdate('INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email,))
        subscription = ConnectionDB.funQuery('SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id,))
    response = { "thread": subscription[0][0], "user": subscription[0][1] }
    return response


def removeSubscription(email, thread_id):
    ConnectionDB.exist(entity="Threads", identificator="id", value=thread_id)
    ConnectionDB.exist(entity="Users", identificator="email", value=email)
    subscription = ConnectionDB.funQuery('SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id,))
    if len(subscription) == 0:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    ConnectionDB.funUpdate('DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id,))
    response = { "thread": subscription[0][0], "user": subscription[0][1] }
    return response        