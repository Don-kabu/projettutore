from django.shortcuts import render, redirect
from.forms import FuiteForm


def accueil(request):
    return render(request, 'accueil.html')
def base(request):
    return render(request , 'base.html')
def signaler(request):
    if request.method == 'POST':
        form = FuiteForm(request.POST, request.FILES)
        latitude = request.POST.get('latitude')
        logitude = request.POST.get('longitude')
        
        if form.is_valid():
            fuite = form.save(commit=False)
            fuite.latitude = latitude
            fuite.longitude = logitude
            fuite.save()
            return redirect('confirmation')
    else:
        form = FuiteForm()
            
    return render(request, 'signaler.html', {'form': form})


