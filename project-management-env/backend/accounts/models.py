from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.user_role = 'PMO'
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, unique=True)
    user_role = models.CharField(
        max_length=3,
        #   PMO = Project Management Office 
        #   PM  = Project Manager
        #   PS  = Project Sponsor
        #   PC  = Project Controller
        #   PSC = Project Scheduler
        #   PP  = Project Planner
        #   AS  = Administrative Staff
        #   U   = Unknown
        choices=[('PMO', 'PMO'), ('PM', 'PM'), ('PS', 'PS'), ('PC', 'PC'),
                    ('PSC', 'PSC'), ('PP', 'PP'), ('AS', 'AS'), ('U', 'U')],  
        default='U'  
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.first_name}'

    def get_email(self):
        return f'{self.email}'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
