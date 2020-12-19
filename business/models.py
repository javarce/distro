
from django.db import models
from business.constants import ROLES


class BaseUser(models.Model):
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=False, null=False)
    first_name = models.CharField(max_length=40, blank=False, null=False)
    last_name = models.CharField(max_length=40, blank=False, null=False)
    username = models.CharField(max_length=20, blank=False, null=False)
    email = models.CharField(max_length=40, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=15, blank=False, null=False, unique=True)
    password = models.CharField(max_length=225, blank=False, null=False)


    def validate(self):
        errors = {}

        if len(self.first_name) > 40:
            errors['error_first_name'] = 'First name cannot be more than 40 characters'

        if not self.first_name:
            errors['error_first_name'] = 'First name cannot be blank'

        if len(self.last_name) > 40:
            errors['error_last_name'] = 'Last name cannot be more than 40 characters'

        if not self.last_name:
            errors['error_last_name'] = 'Last name cannot be blank'

        if len(self.username) > 20:
            errors['error_username'] = 'Username cannot be more than 40 characters'

        if not self.username:
            errors['error_username'] = 'Username cannot be blank'

        if len(self.email) > 40:
            errors['error_email'] = 'Email cannot be more than 40 characters'

        if not self.email:
            errors['error_email'] = 'Email cannot be blank'

        if len(self.phone) > 40:
            errors['error_phone'] = 'Phone cannot be more than 40 characters'

        if not self.phone:
            errors['error_phone'] = 'Phone cannot be blank'

        if len(self.password) > 225:
            errors['error_password'] = 'Password cannot be more than 40 characters'

        if not self.password:
            errors['error_password'] = 'Password cannot be blank'

        return errors

    
    @staticmethod
    def usernameExists(username):
        users = BaseUser.objects.filter(username=username)
        return bool(users)




class Business(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_businesses', null=False, blank=False, default=0)


    def validate(self):
        errors = {}

        if len(self.name) > 100:
            errors['error_name'] = 'Name cannot be more than 100 characters'

        if not self.name:
            errors['error_name'] = 'Name cannot be blank'

        if len(self.location) > 100:
            errors['error_location'] = 'Location cannot be more than 100 characters'

        if not self.location:
            errors['error_location'] = 'Location cannot be blank'

        return errors
