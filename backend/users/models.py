"""
@file models.py
@brief User model for the learning platform.

This module defines the custom User model with additional fields
for profile information and social features.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    @brief Custom user model extending Django's AbstractUser.
    
    @details Adds profile fields including email (used as username),
    avatar, bio, social media links, and timestamps. Uses email
    for authentication instead of username.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    social_media = models.CharField(null=True, blank=True)
    progress = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """
        @brief String representation of the user.
        @return User's email address.
        """
        return self.email

    @property
    def full_name(self):
        """
        @brief Get user's full name.
        
        @return Combined first and last name, stripped of extra whitespace.
        
        @example
        user = User.objects.get(email='john@example.com')
        print(user.full_name)  # "John Doe"
        """
        return f"{self.first_name} {self.last_name}".strip()