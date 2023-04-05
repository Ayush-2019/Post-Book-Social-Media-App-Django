from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, Likes, FollowersCount, PComments
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    for user in user_following:
        following_list.append(user.user)

    following_list.append(request.user.username)

    for names in following_list:
        feed_list = Post.objects.filter(user = names)
        feed.append(feed_list)

    feed_list = list(chain(*feed))

    # people suggestions

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    follow_suggestions = [x for x in list(all_users) if (x not in list(user_following_all))]

    curr_user = User.objects.filter(username = request.user.username)

    final_suggestions = [x for x in list(follow_suggestions) if (x not in list(curr_user))]

    random.shuffle(final_suggestions)

    username_profile = []
    username_profile_list = []

    for user in final_suggestions:
        username_profile.append(user.id)

    for id in username_profile:
        profile_list = Profile.objects.filter(id_user = id)
        username_profile_list.append(profile_list)

    suggestions = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile':user_profile, 'posts':feed_list, 'suggestions_username_profile_list':suggestions[:5]})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Log user in and redirect to settings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #crete a profile obj
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request,'Password doesn\'t match')
            return redirect('signup')
        
    else:

        return render(request, 'signup.html')
    

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        
        else:
            messages.info(request, 'Invalid Credentials!!')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin') 
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()

        return redirect('settings')


    return render(request, 'setting.html', {'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):


    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user = user, image = image, caption = caption)
        new_post.save()
        
        return redirect('/')

    else:
        return redirect('/')
    

@login_required(login_url='signin')
def profile(request, pk):
    user_obj = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_obj)
    user_posts = Post.objects.filter(user = pk)

    posts_length = len(user_posts)
    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower = follower, user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))

    context = {
        'user_object' : user_obj,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower = follower, user = user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()

            return redirect('profile/'+user)
        
        else:
            new_follower = FollowersCount.objects.create(follower = follower, user = user)
            new_follower.save()
            return redirect('profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='signin')   
def search(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    if request.method == 'POST':
        username = request.POST['username']

        username_obj = User.objects.filter(username__icontains=username)

        username_profile = []
        profile_list = []

        for user in username_obj:
            username_profile.append(user.id)

        for ids in username_profile:
            username_profile_list = Profile.objects.filter(id_user = ids)
            profile_list.append(username_profile_list)

        username_profile_list = list(chain(*profile_list))
    return render(request, 'search.html',{'user_profile':user_profile, 'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def delete_post(request, id):
    post = Post.objects.get(id = id)
    post.delete()
    return redirect('/')

@login_required(login_url='signin')
def share_post(request, id):
    post = Post.objects.get(id = id)
    print(post)
    user = request.user.username
    image = post.image
    caption = post.caption
    shared_from = post.user

    new_post = Post.objects.create(user = user, shared_from=shared_from, image = image, caption = caption)
    new_post.save()

    return redirect('/')

@login_required(login_url='signin')
def post(request, id):
    
    selected_post = Post.objects.get(id = id)
    post_comments = PComments.objects.filter(post_id = id)
    comment_value = request.GET.get('comment_value')
    comment_id = request.GET.get('comment_id')

    if comment_value is not None:
        return render(request, 'post.html',{'post':selected_post, 'comments':post_comments, 'comment_value':comment_value, 'comment_id':comment_id})

    else:

        return render(request, 'post.html',{'post':selected_post, 'comments':post_comments})

@login_required(login_url='signin')
def comment(request, id):
    if request.method == 'POST':

        comment = request.POST['comment']
        username = request.user.username
        comment_id = request.GET.get('comment_id')
        post_id = id

        if comment_id is None:
            new_comment = PComments.objects.create(username=username, post_id=post_id, comment=comment)
            new_comment.save()
        
        else:
            comment_obj = PComments.objects.get(id = comment_id)
            comment_obj.comment = comment
            comment_obj.save()

        return redirect('/post/'+id)

    else:
        return redirect('/')
    
@login_required(login_url='signin')
def disable(request, id):

    post = Post.objects.get(id = id)
    if post.comments_disabled == True:
        post.comments_disabled = False

    else:
        post.comments_disabled = True
    post.save()

    return redirect('/')


@login_required(login_url='signin')
def like_in_profile(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    profile_username = request.GET.get('profile')
    from_post = request.GET.get('from_post')

    post = Post.objects.get(id = post_id)

    like_filter = Likes.objects.filter(post_id = post_id, username = username).first()

    if like_filter == None:
        new_like = Likes.objects.create(post_id = post_id, username = username)
        new_like.save()

        post.likes = post.likes+1
        post.save()
    
    else:
        like_filter.delete()
        post.likes = post.likes-1
        post.save()

    if from_post is not None:
            return redirect('/post/' + post_id)

    elif profile_username == None:
        return redirect('/' + '#post_main_'+ post_id)

    else:

        return redirect('/profile/' + profile_username + '#post_position_' + post_id )

