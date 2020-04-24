from django.urls import path
from . import login, candidates, search

urlpatterns = [
    path('', candidates.list_candidates, name='index'),
    path('login/', login.login, name='login'),
    path('logout/', login.logout, name='logout'),
    path('candidates/', candidates.list_candidates, name='list-candidates'),
    path('candidates/new', candidates.new_candidate, name='new-candidate'),
    path('search', search.search, name='search'),
]
