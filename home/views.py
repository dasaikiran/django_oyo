from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Create your views here.


@login_required(login_url="login")
def index(request):
    return render(request, "home/index.html", context={"iterate": range(10)})
