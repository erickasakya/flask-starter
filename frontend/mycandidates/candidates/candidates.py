import requests
import http.client
from django.conf import settings
from django.shortcuts import render, redirect
from .token_validation import validate_token_header


def get_username_from_session(request):
    cookie_session = request.COOKIES.get('session')
    username = validate_token_header(cookie_session,
                                     settings.TOKENS_PUBLIC_KEY)
    if not username:
        return None

    return username


def list_candidates(request):
    '''
    List the user's candidates
    '''
    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    url = settings.CANDIDATES_BACKEND + '/api/me/candidates/'
    headers = {
        'Authorization': request.COOKIES.get('session'),
    }
    result = requests.get(url, headers=headers)
    if result.status_code != http.client.OK:
        return redirect('login')

    context = {
        'candidates': result.json(),
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

    # Only store the candidate if there's a profile url in it
    if profile_url:
        new_url = settings.CANDIDATES_BACKEND + '/api/me/candidates/'
        data = {
            'name': name,
            'profile_url': profile_url,
            'title': title,
            'location': location
        }
        headers = {
            'Authorization': request.COOKIES.get('session'),
        }
        result = requests.post(new_url, data, headers=headers)
        if result.status_code != http.client.CREATED:
            return redirect('login')

    return redirect('list-candidates')
