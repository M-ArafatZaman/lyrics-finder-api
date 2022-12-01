import pytest
from app import create_app

"""
Setup configurations for the app
"""

@pytest.fixture()
def app():
    """
    Create and configure the app and other configurations
    """
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app 


@pytest.fixture()
def client(app):
    """
    Return a test client of the app
    """
    return app.test_client()