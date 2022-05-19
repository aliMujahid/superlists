from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

def index(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
        
    return render(request, 'lists/index.html')

def view_list(request):
    return render(request, 'lists/list.html', {'items':Item.objects.all()})
        