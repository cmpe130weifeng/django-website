from django import forms
from employee_page.models import Employees
class EmployeeCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=14, required=True, label="FirstName")
    last_name = forms.CharField(max_length=16, required=True)
    birth_date = forms.DateField(required=True, label="Date Of Birth (YYYY-MM-DD)")
    gender = forms.CharField(required=True)
    hire_date = forms.DateField(required=True, label="Hire Date (YYYY-MM-DD)")

    class Meta:
        model = Employees
        fields = ('first_name', 'last_name', 'user_name', 'birth_date', 'gender', 'hire_date')
