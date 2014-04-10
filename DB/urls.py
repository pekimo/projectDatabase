from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^db/api/forum/create/$', 'interface.requests.forum.create', name='createForum'),
    url(r'^db/api/forum/details/$', 'interface.requests.forum.details', name='detailsForum'),
    url(r'^db/api/forum/listPosts/$', 'interface.requests.forum.listPosts', name='listPostsForum'),
    url(r'^db/api/forum/listThreads/$', 'interface.requests.forum.listThreads', name='listThreadsForum'),
    url(r'^db/api/forum/listUsers/$', 'interface.requests.forum.listUsers', name='listUsersForum'),
    #----------------------------------------------------------------------------------------------------
    
    url(r'^db/api/post/create/$', 'interface.requests.post.create', name='createPost'),
    url(r'^db/api/post/details/$', 'interface.requests.post.details', name='detailsPost'),
    url(r'^db/api/post/list/$', 'interface.requests.post.list', name='listPost'),
    url(r'^db/api/post/remove/$', 'interface.requests.post.remove', name='removePost'),
    url(r'^db/api/post/restore/$', 'interface.requests.post.restore', name='restorePost'),
    url(r'^db/api/post/update/$', 'interface.requests.post.update', name='updatePost'),
    url(r'^db/api/post/vote/$', 'interface.requests.post.vote', name='votePost'),
    #----------------------------------------------------------------------------------------------------
    
    url(r'^db/api/user/create/$', 'interface.requests.user.create', name='createUser'),
    url(r'^db/api/user/details/$', 'interface.requests.user.details', name='detailsUser'),
    url(r'^db/api/user/follow/$', 'interface.requests.user.follow', name='followUser'),
    url(r'^db/api/user/listFollowers/$', 'interface.requests.user.listFollowers', name='listFollowersUser'),
    url(r'^db/api/user/listFollowing/$', 'interface.requests.user.listFollowing', name='listFollowingUser'),
    url(r'^db/api/user/listPosts/$', 'interface.requests.user.listPosts', name='listPostsUser'),
    url(r'^db/api/user/unfollow/$', 'interface.requests.user.unfollow', name='unfollowUser'),
    url(r'^db/api/user/updateProfile/$', 'interface.requests.user.updateProfile', name='updateProfileUser'),
    #-----------------------------------------------------------------------------------------------------
    
    url(r'^db/api/thread/close/$', 'interface.requests.thread.close', name='closeThread'),
    url(r'^db/api/thread/create/$', 'interface.requests.thread.create', name='createThread'),
    url(r'^db/api/thread/details/$', 'interface.requests.thread.details', name='detailsThread'),
    url(r'^db/api/thread/list/$', 'interface.requests.thread.list', name='listThread'),
    url(r'^db/api/thread/listPosts/$', 'interface.requests.thread.listPosts', name='listPostsThread'),
    url(r'^db/api/thread/open/$', 'interface.requests.thread.open', name='openThread'),
    url(r'^db/api/thread/remove/$', 'interface.requests.thread.remove', name='removeThread'),
    url(r'^db/api/thread/restore/$', 'interface.requests.thread.restore', name='restoreThread'),
    url(r'^db/api/thread/subscribe/$', 'interface.requests.thread.subscribe', name='subscribeThread'),
    url(r'^db/api/thread/unsubscribe/$', 'interface.requests.thread.unsubscribe', name='unsubscribeThread'),
    url(r'^db/api/thread/update/$', 'interface.requests.thread.update', name='updateThread'),
    url(r'^db/api/thread/vote/$', 'interface.requests.thread.vote', name='voteThread'),
    #--------------------------------------------------------------------------------------------------------
)
