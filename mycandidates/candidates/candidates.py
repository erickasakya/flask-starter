from django.shortcuts import render, redirect
from .models import CandidateModel, SessionModel


def get_username_from_session(request):
    cookie_session = request.COOKIES.get('session')
    try:
        session = SessionModel.objects.get(session=cookie_session)
    except SessionModel.DoesNotExist:
        return None

    return session.username


def list_candidates(request):
    '''
    List the user's candidates
    '''
    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    user_candidates = (CandidateModel.objects
                       .filter(username=username)
                       .order_by('-timestamp'))

    context = {
        'candidates': user_candidates,
        'username': username,
    }
    return render(request, 'list_candidates.html', context)


def new_candidate(request):
    '''
    Create a new candidate for the user
    '''
    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    profile_url = request.POST.get('profileUrl')
    name = request.POST.get('name')
    title = request.POST.get('title')
    location = request.POST.get('location')

    if profile_url:
        # Only store the candidate if there's text in it
        new_candidate = CandidateModel(profile_url=profile_url, username=username, name=name, title=title,
                                       location=location)
        new_candidate.save()

    return redirect('list-candidates')
