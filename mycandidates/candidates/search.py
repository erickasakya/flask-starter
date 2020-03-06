from django.shortcuts import render

from .models import CandidateModel
from .candidates import get_username_from_session


def search(request):
    username = get_username_from_session(request)
    search_param = request.GET.get('search')

    results = (CandidateModel.objects
               .filter(name__icontains=search_param)
               .order_by('-timestamp'))

    context = {
        'candidates': results,
        'username': username,
    }
    return render(request, 'search.html', context)
