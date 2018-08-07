from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item
# Create your views here.
def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request,'home.html')
        if request.method =='POST':
            new_item_text = request.POST['item_text']
            Item.objects.create(text=new_item_text)
            return redirect('/')
        #create not requiring saving
    # else :
    #     new_item_text= ''
        items = Item.objects.all()
        return render(request, 'home.html', {'items': items})

    #
    #     'new_item_text' : new_item_text
    # })