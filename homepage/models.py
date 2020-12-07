from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from employee_page.models import *

# Create your models here.

class UserProfile(models.Model):

    emp_no = models.ForeignKey(Employees, on_delete=models.CASCADE)
    dept_no = models.ForeignKey(Departments, on_delete=models.CASCADE)
    user_name_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __unicode__(self):  # __str__
        return self.user_name.user_name_profile