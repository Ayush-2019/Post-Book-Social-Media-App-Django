from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('comment/<str:id>', views.comment, name='comment'),
    path('disable/<str:id>', views.disable, name='disable'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('post/<str:id>', views.post, name='post'),
    path('delete-post/<str:id>', views.delete_post, name='delete_post'),
    path('share-post/<str:id>', views.share_post, name='share_post'),
    path('like', views.like, name='like'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name='upload')
]