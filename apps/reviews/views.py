from django.shortcuts import redirect, render, get_object_or_404
from .forms import ReviewForm
from .models import Review

# Create your views here.


def review_create(request, product_pk):
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_pk
            review.save()
    return redirect('products:product_detail', pk=product_pk)


def review_list(request):
    reviews = Review.objects.filter(approved=True)
    return render(request, 'reviews/review_list.html', {'reviews': reviews})