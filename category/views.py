from django.shortcuts import render
from category.models import Category


# This function for add category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        category_image = request.FILES.get('category_image')

        categories = Category.objects.create(
            category_name=category_name,
            description=description,
            category_image=category_image
        )
        categories.save()

    return render(request, 'category/add-category.html')


# This function for manage category
def manage_category(request):
    categories = Category.objects.all()
    context = {
		'categories': categories,
	}
    print(categories)
    return render(request, 'category/manage-category.html', context)