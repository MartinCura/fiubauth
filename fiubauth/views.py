from django.shortcuts import render
from oidc_provider.models import UserConsent

def user_home(request):
    print(request.user.username)
    consents = UserConsent.objects.filter(user__username=request.user.username)
    return render(request, 'home.html', {'consents': consents})
