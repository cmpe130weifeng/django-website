from django.shortcuts import render
from django.http import HttpResponse, Http404

from employee_page.models import *
from homepage.models import *

from django.db import connection
from utils.db_utils import *
# Create your views here.

def index(request):
     if request.method == "POST":
          employee_name = request.POST.get('search_employee')
       

          employee_name_list = employee_name.split()
     
          print(employee_name_list)

     try:
          if request.method == "POST":
               employee_name = request.POST.get('search_employee')
               first_name = employee_name.split()[0]
               last_name = employee_name.split()[1]
            
          else:
               first_name = request.user.first_name
               last_name = request.user.last_name

          employee_record = Employees.objects.get(first_name=first_name, last_name=last_name)  
          records = return_employee_details(employee_record.emp_no, connection) 
          dept_name = ""
          
          for record in records:
               if (record.dept_name):
                    dept_name = record.dept_name
          dept_record = Departments.objects.get(dept_name=dept_name) 
          
     except Employees.DoesNotExist:
        raise Http404

     variables = { 'current_page': 'employee_page' , 'records': records, 'dept_record': dept_record}
     
     return render(request, 'employee.html', variables)

def request_insight(request, dept_id):
     
     try:
          print(dept_id)
          print(type(dept_id)) 

          records = return_emp_count_for_dept(connection, dept_id)
          records_genders = return_dept_gender_count(connection, dept_id)

          first_name = request.user.first_name
          last_name = request.user.last_name

          employee_record = Employees.objects.get(first_name=first_name, last_name=last_name)  
          emp_records = return_employee_details(employee_record.emp_no, connection) 
          dept_name = ""
          
          for record in emp_records:
               if (record.dept_name):
                    dept_name = record.dept_name
          dept_record = Departments.objects.get(dept_name=dept_name) 
          print(records)
          print(records_genders)
     
     except Employees.DoesNotExist:
        raise Http404 

     variables = { 'current_page': 'employee_page', 'records': records, 'records_genders': records_genders, 'dept_record': dept_record }
     return render(request, 'insight.html', variables)

def request_employee_information(request, id):
     
     employee = Employees.objects.get(emp_no=id)

     if request.method == "POST":
          
          if employee.first_name != request.POST.get('first_name'):
               employee.first_name = request.POST.get('first_name')
          elif employee.last_name != request.POST.get('last_name'):
               employee.last_name = request.POST.get('last_name')
          elif employee.user_name != request.POST.get('user_name'):
               employee.user_name = request.POST.get('user_name')

          employee.save()
     try:
        
        variables = { 'employee': employee }
     except Employees.DoesNotExist:
        raise Http404
     return render(request, 'employee_information.html', variables)

