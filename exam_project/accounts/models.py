from django.contrib.auth import models as auth_models
from django.db import models


class AppUser(auth_models.AbstractUser):

    first_name = models.CharField(max_length=30, null=True, blank=True, )
    last_name = models.CharField(max_length=30, null=True, blank=True, )
    money = models.PositiveIntegerField(default=0, null=False, blank=True, )
    profile_picture = models.URLField(null=True, blank=True, )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
