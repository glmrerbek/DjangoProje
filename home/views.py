from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.models import ContactFormMessage, ContactFormu, Setting, UserProfile
from django.contrib import messages
from kurumsal.models import Category, Comment, Images, Kurumsal
from home.forms import SearchForm, SignUpForm
import json
from django.contrib.auth import authenticate, login, logout
from content.models import CImages, Content, Menu
# Create your views here.


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Kurumsal.objects.all()[:5]
    menu = Menu.objects.all()
    category = Category.objects.all()
    haberler = Kurumsal.objects.all().order_by('-id')[:4]
    duyrular = Content.objects.filter(type='duyuru', status='True').order_by('-id')[:4]
    context = {'setting': setting,
               'page': 'home',
               'sliderdata': sliderdata,
               'category': category,
               'haberler': haberler,
               'duyrular': duyrular,
               'menu': menu,}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'hakkimizda', 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'referanslar', 'category': category}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.save()  # verirabanına kaydet
            messages.success(
                request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz ")
            return HttpResponseRedirect('/iletisim')
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form, 'category': category, }
    return render(request, 'iletisim.html', context)


def category_kurumsals(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    kurumsals = Kurumsal.objects.filter(category_id=id)
    context = {'kurumsals': kurumsals,
               'category': category, 'categorydata': categorydata}
    return render(request, 'details.html', context)


def kurumsal_detail(request, id, slug):
    category = Category.objects.all()
    kurumsal = Kurumsal.objects.get(pk=id, slug=slug)
    images = Images.objects.filter(kurumsal_id=id)
    comments = Comment.objects.filter(kurumsal_id=id, status='True')
    context = {'category': category,
               'kurumsal': kurumsal,
               'images': images,
               'comments': comments, }
    return render(request, 'kurumsal_detail.html', context)


def kurumsal_search(request):
    if request.method == 'POST':  # Chect form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            kurumsal = Kurumsal.objects.filter(title__icontains=query)
            context = {'kurumsal': kurumsal,
                       'category': category, }
            return render(request, 'kurumsal_search.html', context)
            
    return HttpResponseRedirect('/')


def kurumsal_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        kurumsal = Kurumsal.objects.filter(title__icontains=q)
        results = []
        for rs in kurumsal:
            kurumsal_json = {}
            kurumsal_json = rs.title
            results.append(kurumsal_json)
            data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            messages.warning(
                request, "Login Hatasi ! kullanici adi veya Sifre yanlis")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category, }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(
                request, "Hoş Geldiniz.. Sitemize başarılı bir şekilde üye oldunuz.")
            return HttpResponseRedirect('/home')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form, }

    return render(request, 'signup.html', context)


def menu(request, id):
    content = Content.objects.get(menu_id=id)
    if content:
        link = '/content/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    else:
        messages.warning(request, "Hata ! İlgili içerik bulunamadı ")
        link = '/'
        return HttpResponseRedirect(link)
