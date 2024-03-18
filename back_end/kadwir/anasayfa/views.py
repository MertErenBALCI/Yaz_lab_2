from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return redirect('homePage')

def homePage(request):
    
    return render(request, "kadwir.html")

def cikis(request):
    request.session.clear()
    return redirect('home')

def oncekiSayfa(request):
    
    return redirect('home')

def yonetici(request):
    return render(request, "admin.html")

def antrenor(request):
    return render(request, "antrenor.html")

def danisman(request):
    return render(request, "danisman.html")