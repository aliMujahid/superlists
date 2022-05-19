from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item, List

def index(request):    
    return render(request, 'lists/index.html')

def view_list(request):
    return render(request, 'lists/list.html', {'items':Item.objects.all()})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')         