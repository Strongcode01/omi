from django.shortcuts import render, redirect, get_object_or_404
from .forms import DiagnosticRequestForm
from .models import DiagnosticRequest

# Create your views here.


def request_list(request):
    reqs = DiagnosticRequest.objects.filter(user=request.user)
    return render(request, 'diagnostics/request_list.html', {'requests': reqs})


def request_create(request):
    if request.method=='POST':
        form = DiagnosticRequestForm(request.POST)
        if form.is_valid():
            dr = form.save(commit=False)
            dr.user = request.user
            dr.save()
            return redirect('diagnostics:request_list')
    else:
        form = DiagnosticRequestForm()
    return render(request, 'diagnostics/request_form.html', {'form': form})


def request_detail(request, pk):
    dr = get_object_or_404(DiagnosticRequest, pk=pk, user=request.user)
    return render(request, 'diagnostics/request_detail.html', {'request_obj': dr})