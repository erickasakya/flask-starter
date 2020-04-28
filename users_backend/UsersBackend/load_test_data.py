from users_backend.app import create_app
from users_backend.models import UserModel


if __name__ == '__main__':
    application = create_app(script=True)
    application.app_context().push()

    # Create some test data
    test_data = [
        # username, timestamp, text
        ('fabricio', "password", "1962-05-01 00:00:00Z"),
        ('mariano', "password", "1963-06-01 00:00:00Z"),
        ('ariel', "password", "1962-05-01 00:00:00Z"),
        ('agustina', "password", "1963-06-01 00:00:00Z"),
        ('cristian', "password", "1962-05-01 00:00:00Z"),
    ]
    for username, password, creation in test_data:
        user = UserModel(username=username, password=password,
                         creation=creation)
        application.db.session.add(user)

    application.db.session.commit()
