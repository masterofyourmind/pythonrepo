from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from programmer.models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from datetime import datetime, date
from .models import Post, BlogComment
from .templatetags import extras
import re
from time import strftime, gmtime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    allPost = Post.objects.all()
    context = {'allPosts': allPost}
    return render(request, 'index.html', context)

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "please enter valid username or password")
            return redirect("home")

    return redirect("home")

def logoutUser(request):
    logout(request)
    messages.success(request, "You are successfully logged out, Have a good day!!")
    return redirect("home")

def signup(request):
    if request.method=='POST':
        # Get the post parameter
        username=request.POST['username']
        fname= request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #Check for error
        if len(username)>10:
            messages.warning(request, "username must be under 10 characters")
            return redirect("/")
        if not username.isalnum():
            messages.error(request, "Username only contain letters and numbers")
            return redirect("/")
        if pass1 != pass2:
            messages.warning(request, "Enter the same password in both fileds")
            return redirect("/")
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "your account has been successfully created")
        return redirect("/")
    else:
        return HttpResponse("404 not found")

def contact(request):
    li = []
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if request.method=="POST":
        name = request.POST.get('name')
        emailNum = request.POST.get('email')
        if(re.search(regex,emailNum)):
            email = emailNum
        else:  
            messages.error(request, "Enter the valid email !")
            return redirect('contact')
        phoneNum = request.POST.get('phone')
        for i in range(len(phoneNum)):
            if phoneNum[i].isdigit():
                li.append(phoneNum[i])
            else:
                messages.error(request, "Don't use alphabet or special characters or '+' in Phone Number")
                return redirect('contact')
        phone = ''.join([str(elem) for elem in li])
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your message sent successfully")
    return render(request, 'contact.html')

def all_users(request):
    userlist = User.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(userlist, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user_list.html', {'users': users})



def BlogDetailView(request, slug):
    showtime = strftime("%Y-%m-%d %H:%M:%S")
    post = Post.objects.filter(slug=slug).filter(timestamp__lte = showtime).first()
    if post == None:
        return render(request, 'error_404.html')
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog_detail.html', context)

def postComment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if postSno=="":
            messages.error(request, 'please donot post somthing randomly')
            return redirect("/")
        if comment == "":
            messages.error(request, 'Please write something before submit')
            return redirect(f"/{post.slug}")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment added successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Reply added successfully")
    return redirect(f"/{post.slug}")

def about(request):
    return render(request, 'about.html')

def exams(request):
    return render(request, 'pycomp.html')

def teams(request):
    return render(request, 'team_details.html')


#Error page loader
def custom_page_not_found_view(request, exception):
    return render(request, "error_404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "error_404.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "error_404.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "error_404.html", {})
#Error page loader end