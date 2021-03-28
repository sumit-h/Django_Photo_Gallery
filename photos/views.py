from django.shortcuts import render, redirect
from .models import Category,Photo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from PIL import Image
import random


# Create your views here.
def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()

    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    
    
    paginator = Paginator(photos,8)

    p = paginator.num_pages
    # print(p)
    page_num = request.GET.get('page',1)

    try:
        page = paginator.page(page_num)
    
    except EmptyPage:
        page = paginator.page(1)

   

    l = range(1,p)



    context = {
        'categories':categories,
        'photos':page,
        'p':l,
        'category':category,

    }
    return render(request,'photos/gallery.html',context)


def viewPhoto(request,pk):
    a=random.randint(0, 10000)
    b=random.randint(0, 10000)
    photo = Photo.objects.get(id=pk)
    
    angle = (request.GET.get('angle'))
    if angle == '90':
        im = Image.open(photo.image).rotate(90)
        image = im.save(r"static\\images\\newq1_{}_{}.jpg".format(a,b))
        Photo.objects.filter(id=pk).update(image = "newq1_{}_{}.jpg".format(a,b) )
        
        
        

    elif angle == '-90':
        im = Image.open(photo.image).rotate(-90)
        image = im.save(r"static\\images\\newq1_{}_{}.jpg".format(a,b))
        Photo.objects.filter(id=pk).update(image = "newq1_{}_{}.jpg".format(a,b) )


    
    
    
    
    
    return render(request,'photos/photo.html',{"photo":photo})
    

def addPhoto(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        
        
        if data['category'] != 'none':
            category = Category.objects.get(name=data['category'])
        
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])

        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category = category,
                image = image
            )

        return redirect("gallery")

    context = {
        'categories':categories, }
    return render(request,'photos/add.html',context)


