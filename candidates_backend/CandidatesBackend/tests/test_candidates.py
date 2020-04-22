'''
Test the Candidates operations


Use the candidate_fixture to have data to retrieve,
it generates three candidates
'''
from unittest.mock import ANY
import http.client
from freezegun import freeze_time
from .constants import PRIVATE_KEY
from candidates_backend import token_validation
from faker import Faker
fake = Faker()


@freeze_time('2019-05-07 13:47:34')
def test_create_me_candidate(client):
    new_candidate = {
        'username': fake.name(),
        'name': fake.text(50),
        'title': fake.text(240),
        'location': fake.text(240),
        'profile_url': fake.text(240),
    }
    header = token_validation.generate_token_header(fake.name(),
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/candidates/', data=new_candidate,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'username': ANY,
        'name': new_candidate['name'],
        'title': new_candidate['title'],
        'location': new_candidate['location'],
        'profile_url': new_candidate['profile_url'],
        'timestamp': '2019-05-07T13:47:34',
    }
    assert result == expected


def test_create_me_unauthorized(client):
    new_candidate = {
        'username': fake.name(),
        'name': fake.text(50),
        'title': fake.text(240),
        'location': fake.text(240),
        'profile_url': fake.text(240),
    }
    response = client.post('/api/me/candidates/', data=new_candidate)
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_me_candidates(client, candidate_fixture):
    username = fake.name()
    name = fake.text(50)
    title = fake.text(240)
    location = fake.text(240)
    profile_url = fake.text(240)

    # Create a new candidate
    new_candidate = {
        'name': name,
        'title': title,
        'location': location,
        'profile_url': profile_url
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/candidates/', data=new_candidate,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    # Get the candidates of the user
    response = client.get('/api/me/candidates/', headers=headers)
    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 1
    result = results[0]
    expected_result = {
        'id': ANY,
        'username': username,
        'name': name,
        'title': title,
        'location': location,
        'profile_url': profile_url,
        'timestamp': ANY,
    }
    assert result == expected_result


def test_list_me_unauthorized(client):
    response = client.get('/api/me/candidates/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_candidates(client, candidate_fixture):
    response = client.get('/api/candidates/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing
    previous_id = -1
    for candidate in result:
        expected = {
            'name': ANY,
            'title': ANY,
            'location': ANY,
            'profile_url': ANY,
            'username': ANY,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == candidate
        assert candidate['id'] > previous_id
        previous_id = candidate['id']


def test_list_candidates_search(client, candidate_fixture):
    username = fake.name()
    new_candidate = {
        'username': username,
        'name': 'Fabricio',
        'title': 'Software Engineer',
        'location': 'Remote',
        'profile_url': 'https://www.linkedin.com/in/fabriciopautasso/'
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/candidates/', data=new_candidate,
                           headers=headers)
    assert http.client.CREATED == response.status_code

    response = client.get('/api/candidates/?search=Fab')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the returned values contain "Fabricio"
    for candidate in result:
        expected = {
            'name': ANY,
            'title': ANY,
            'location': ANY,
            'profile_url': ANY,
            'username': username,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == candidate
        assert 'fabricio' in candidate['name'].lower()


def test_get_candidate(client, candidate_fixture):
    candidate_id = candidate_fixture[0]
    response = client.get(f'/api/candidates/{candidate_id}/')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'name' in result
    assert 'title' in result
    assert 'location' in result
    assert 'profile_url' in result
    assert 'username' in result
    assert 'timestamp' in result
    assert 'id' in result


def test_get_non_existing_candidate(client, candidate_fixture):
    candidate_id = 123456
    response = client.get(f'/api/candidates/{candidate_id}/')

    assert http.client.NOT_FOUND == response.status_code
