from store.models import Category

def categories(request):
    main_categories = Category.objects.filter(parent__isnull=True)
    return {'main_categories': main_categories}