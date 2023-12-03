from django.contrib.auth.models import AbstractUser, GroupManager
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
