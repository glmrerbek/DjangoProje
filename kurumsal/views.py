from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from kurumsal.models import Comment, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return HttpResponse("kurumsal Page")


@login_required(login_url='/login')  # check login
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user  # Access User Session information
            data = Comment()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.kurumsal_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            # Client computer ip address
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # verirabanına kaydet
            messages.success(
                request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz ")
            return HttpResponseRedirect(url)
            # return HttpResponse("Kaydedildi")
            messages.warning(
                request, "Yorumunuz Kaydedilmedi. Lutfen Kontrol Ediniz ")

        return HttpResponseRedirect(url)
