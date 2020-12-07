from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from employee_page.models import Employees
from utils.db_utils import return_departments, return_all_titles_dropdown
from django.db import connection

class UpdateEmpDeptForm(forms.Form):
    emp_no = forms.IntegerField(required=True, label="Employee Number")
    # dept_no = forms.CharField(required=True, label="dept_no")
    from_date = forms.DateField(required=True, label="From Date")
    dept_no = forms.ChoiceField(
        choices=return_departments(connection), label="Department", required=False
    )
    is_manager = forms.ChoiceField(choices=[(0, "No"), (1, "Yes")], label="Manager?")
    title = forms.ChoiceField(
        choices=return_all_titles_dropdown(connection), label="Title", required=False
    )
    salary = forms.IntegerField(required=False)


class EmployeeCreateForm(forms.Form):
    first_name = forms.CharField(max_length=14, required=True, label="First Name")
    last_name = forms.CharField(max_length=16, required=True, label="Last Name")
    user_name = forms.CharField(max_length=14, required=True, label="User Name")
    gender = forms.ChoiceField(
        choices=[("M", "Male"), ("F", "Female")], required=True, label="Gender"
    )
    birth_date = forms.DateField(required=True, label="Date of Birth (YYYY-MM-DD)")
    hire_date = forms.DateField(required=True, label="Hire Date")
    salary = forms.IntegerField(required=True, label="Salary")
    dept_no = forms.ChoiceField(
        choices=return_departments(connection), required=True, label="Department"
    )
    is_manager = forms.ChoiceField(
        choices=[(0, "No"), (1, "Yes")], label="Manager?", required=True
    )
    title = forms.ChoiceField(
        choices=return_all_titles_dropdown(connection), label="Title", required=True
    )


class AddDeptForm(forms.Form):
    dept_name = forms.CharField(required=True, max_length=40)

    def clean_dept_name(self):
        cursor = connection.cursor()
        dept_name = self.cleaned_data.get("dept_name")
        print(dept_name)
        sql = "SELECT COUNT(*) FROM department where lower(dept_name) = %s"
        bind = [dept_name]
        cursor.execute(sql, bind)
        dept_cnt = cursor.fetchone()[0]

        if dept_cnt > 0:
            raise forms.ValidationError("Department already exists")

        return dept_name