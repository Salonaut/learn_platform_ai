"""
Shared test configuration and fixtures.

This file can be used if migrating to pytest in the future.
For now, it serves as documentation for common test patterns.
"""

# If using pytest, uncomment and use these fixtures:
#
# import pytest
# from users.tests.factories import UserFactory
#
#
# @pytest.fixture
# def user():
#     """Create a standard user for testing."""
#     return UserFactory()
#
#
# @pytest.fixture
# def active_user():
#     """Create an active user for testing."""
#     return UserFactory(is_active=True)
#
#
# @pytest.fixture
# def inactive_user():
#     """Create an inactive user for testing."""
#     return UserFactory(is_active=False)
#
#
# @pytest.fixture
# def user_with_password():
#     """Create a user with a known password."""
#     return UserFactory(password='TestPassword123!')
#
#
# @pytest.fixture
# def api_client():
#     """Create a DRF API client."""
#     from rest_framework.test import APIClient
#     return APIClient()
#
#
# @pytest.fixture
# def authenticated_client(user):
#     """Create an authenticated API client."""
#     from rest_framework.test import APIClient
#     client = APIClient()
#     client.force_authenticate(user=user)
#     return client
