from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from kurumsal.models import Category, Comment
from home.models import UserProfile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from user.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from content.models import Content, ContentForm, Menu


# Create your views here.
@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user=request.user
    profile= UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,'profile': profile,}
    return render(request, 'user_profile.html',context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user session data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
        profile_form.save()
        messages.success(request, 'Your account has been updated!')
        return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form' : profile_form
        }
        return render (request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save ()
            update_session_auth_hash(request, user) # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category
    })


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted...')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()  # verirabanına kaydet
            messages.success(request, 'Your Content Insterted Successfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(
                request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'category': category,
            'form': form,
            'menu': menu, }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')  # Check login
def contentedit(request, id):
    content = Content.objects.get(id=id)
    menu = Menu.objects.all()
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Content Updated Successfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(
                request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' + str(id))
    else:
        category = Category.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category': category,
            'form': form,
            'menu': menu, }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'menu': menu,
        'contents': contents,
    }
    return render(request, 'user_contents.html', context)


@login_required(login_url='/login')  # Check login
def contentdelete(request, id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content deleted..')
    return HttpResponseRedirect('/user/contents')
