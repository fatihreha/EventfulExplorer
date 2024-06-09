from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm
from .models import profile
from main.models import event
from django.core.mail import send_mail

# Login request
def login_request(request):
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

# Signup request
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

# View profile
def viewProfile(request):
    events = event.objects.filter(orginzer=request.user)
    return render(request, 'profile/profile.html', {'events': events})

# View user profile
def view_user_profile(request, user_id):
    userobj = User.objects.get(id=user_id)
    events = event.objects.filter(orginzer=userobj)
    return render(request, 'profile/view_profile.html', {'userInfo': userobj, 'events': events})

@csrf_exempt
def updateinfo(request):
    if request.method == 'POST':
        fn = request.POST.get('fn')
        ln = request.POST.get('ln')
        em = request.POST.get('em')
        un = request.POST.get('un')
        obj = User.objects.get(pk=request.user.id)
        obj.first_name = fn
        obj.last_name = ln
        obj.email = em
        obj.username = un
        obj.save()
        data = {'firstName': obj.first_name, 'lastName': obj.last_name, 'email': obj.email, 'uname': obj.username}
        return JsonResponse({'status': 1, 'msg': 'User Updated Successfully!', 'obj': data})

@csrf_exempt
def updatePic(request):
    if request.method == 'POST':
        obj = profile.objects.get(user=request.user)
        image = request.FILES.get('profilePic')
        obj.profilePic = image
        obj.save()
        image_url = obj.profilePic.url
        return JsonResponse({'status': 1, 'img': image_url})

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        follower = request.user
        userID = request.POST.get('userID')
        followed = profile.objects.get(user=userID)
        if follower not in followed.followers.all():
            followed.followers.add(follower)
            status = 1  # return 1 if follow
        else:
            followed.followers.remove(follower)
            status = 0  # return 0 if unfollow
        return JsonResponse({'status': status})

@csrf_exempt
def updateProfile(request):
    if request.method == 'POST':
        bio = request.POST.get('bio')
        mb = request.POST.get('mb')
        pf = profile.objects.get(user_id=request.user.id)
        pf.bio = bio
        pf.phone = mb
        pf.save()
        data = {'bio': bio, 'mobile': mb}
        return JsonResponse({'status': 1, 'msg': 'User Updated Successfully!', 'obj': data})

@csrf_exempt
def updateCompany(request):
    if request.method == 'POST':
        name = request.POST.get('company_name')
        description = request.POST.get('profile_description')
        pf = profile.objects.get(user_id=request.user.id)
        pf.company_name = name
        pf.description = description
        pf.save()
        data = {'name': name, 'description': description}
        return JsonResponse({'status': 1, 'msg': 'Company Updated Successfully!', 'obj': data})
