import pytest
import http.client
from candidates_backend.app import create_app
from .constants import PRIVATE_KEY
from candidates_backend import token_validation
from faker import Faker
fake = Faker()


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def candidate_fixture(client):
    '''
    Generate three candidates in the system.
    '''

    candidate_ids = []
    for _ in range(3):
        candidate = {
            'name': fake.text(240),
            'title': fake.text(240),
            'location': fake.text(240),
            'profile_url': fake.text(240),
        }
        header = token_validation.generate_token_header(fake.name(),
                                                        PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post('/api/me/candidates/', data=candidate,
                               headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        candidate_ids.append(result['id'])

    yield candidate_ids

    # Clean up all candidates
    response = client.get('/api/candidates/')
    candidates = response.json
    for candidate in candidates:
        candidate_id = candidate['id']
        url = f'/admin/candidates/{candidate_id}/'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code
