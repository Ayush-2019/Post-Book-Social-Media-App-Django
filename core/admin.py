from django.contrib import admin
from .models import Profile, Post, Likes, FollowersCount, PComments
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(FollowersCount)
admin.site.register(PComments)