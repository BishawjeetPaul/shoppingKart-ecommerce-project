from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
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
    categories = Category.objects.filter(isDelete=False)
    context = {
		'categories': categories,
	}
    print(categories)
    return render(request, 'category/manage-category.html', context)


# This function is use for edit category
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {'category': category}

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('description')

        try:
            category.category_name = category_name
            category.category_description = category_description
            # Handle image upload
            if request.FILES.get('category_image'):
                category.category_image = request.FILES['category_image']

            # Update category model
            category.save()

            # messages.success(request, "Successfully Updated Category")
            return redirect('manage-category')  # ✅ redirect instead of HttpResponseRedirect

        except Exception as e:
            # messages.error(request, f"Failed to Update Category: {str(e)}")
            return redirect('edit-category', category_id=category.id)  # ✅ redirect back to edit page

    return render(request, 'category/edit-category.html', context)


# This function is use for delete category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.isDelete=True
    category.save()
    return redirect('manage-category')
