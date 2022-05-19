from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        return render(request, 'lists/index.html', {"new_item_text":request.POST['item_text']})
    return render(request, 'lists/index.html')