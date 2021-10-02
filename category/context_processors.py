from .models import Category

def menu_links(request):
    cat_links = Category.objects.all()

    return dict(cat_links=cat_links)