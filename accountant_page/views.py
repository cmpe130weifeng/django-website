from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from accountant_page.forms import  *
from employee_page.models import *
from django.db import connection
from django.contrib.auth.models import User

from utils.db_utils import *
# Create your views here.

def index(request):
     employees = Employees.objects.all()
     variables = { 'current_page': 'accountant_page', 'employees': employees }
     
     return render(request, 'accountant.html', variables)

def add_employee(request):
    
    form = EmployeeCreateForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        dept_no = form.cleaned_data.get("dept_no")
        hire_date = form.cleaned_data.get("hire_date")
        is_manager = form.cleaned_data.get("is_manager")
        title = form.cleaned_data.get("title")
        salary = form.cleaned_data.get("salary")
        birth_date = form.cleaned_data.get("birth_date")
        gender = form.cleaned_data.get("gender")

        emp_no = add_employee_record(
            connection, first_name, last_name, hire_date, gender, birth_date
        )
        print(emp_no)
        update_employee_dept(
            emp_no,
            dept_no,
            hire_date,
            connection,
        )
        print("is_manager = ", is_manager, type(is_manager))
        if is_manager == "1":
            add_dept_manager(connection, dept_no, emp_no, hire_date)

        update_emp_title(connection, emp_no, title, hire_date)

        update_emp_salary(connection, emp_no, salary, hire_date)

        userName = form.cleaned_data.get("user_name")
        user = User.objects.create_user(username=userName, email=" ", first_name=first_name, last_name=last_name, password='123456')
        user.save()
        return redirect('/accountant_page/index/')
    
    form = EmployeeCreateForm()
    title = "Please Add The Employee Information"

    return render(request, "accountant_options.html", {"form": form, "title": title})
    
def request_employee_information(request, id):
     
     employee = Employees.objects.get(emp_no=id)

     if request.method == "POST":
          
          if employee.first_name != request.POST.get('first_name'):
               employee.first_name = request.POST.get('first_name')
          elif employee.last_name != request.POST.get('last_name'):
               employee.last_name = request.POST.get('last_name')
          elif employee.emp_no != request.POST.get('emp_no'):
               employee.emp_no = request.POST.get('emp_no')

          employee.save()
     try:
        
        variables = { 'records': employee }
     except Employees.DoesNotExist:
        raise Http404
     return render(request, 'employee_information.html', variables)

def update_emp_dept_view(request):
    form = UpdateEmpDeptForm(request.POST or None)
    if form.is_valid():
        emp_no = form.cleaned_data.get("emp_no")
        dept_no = form.cleaned_data.get("dept_no")
        from_date = form.cleaned_data.get("from_date")
        is_manager = form.cleaned_data.get("is_manager")
        title = form.cleaned_data.get("title")
        salary = form.cleaned_data.get("salary")
        print(form.cleaned_data)
        if dept_no != "":
            update_employee_dept(
                emp_no,
                dept_no,
                from_date,
                connection,
            )
        if is_manager == "1":
            add_dept_manager(connection, dept_no, emp_no, from_date)

        if title:
            update_emp_title(connection, emp_no, title, from_date)

        if salary:
            update_emp_salary(connection, emp_no, salary, from_date)
        return redirect('/accountant_page/index/')
    
    title = "Please Update The Employee Information"
    return render(request, "accountant_options.html", { "form": form, "title": title})

def add_department_view(request):
    form = AddDeptForm(request.POST or None)
    
    print(form.is_valid())

    if form.is_valid():
        print(form.cleaned_data)
        dept_name = form.cleaned_data.get("dept_name")
        add_department(connection, dept_name)
        return redirect('/accountant_page/index/')

    title = "Please Add The Departemnt Information"

    return render(request, "accountant_options.html", {"form": form, "title": title})

def admin_insight_view(request):
    
    try:
        records = return_all_dept_emp_count(connection)
        print(records)
        records_genders = return_all_dept_gender_count(connection)
        print(records_genders)
    
    except Employees.DoesNotExist:
        raise Http404 

    variables = { 'current_page': 'accountant_page', 'records': records, 'records_genders': records_genders }
    return render(request, "admin_insight.html", variables)


