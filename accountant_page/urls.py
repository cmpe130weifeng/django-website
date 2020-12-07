from django.urls import include, path
from accountant_page import views

app_name = 'accountant_page'

urlpatterns = [
    path('index/', views.index, name='index'),

    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_department/', views.add_department_view, name = "add_department"),
    
    path("employee_information/<int:id>/", views.request_employee_information, name = "employee_detail_view"),
    path("update_employee/", views.update_emp_dept_view, name="update_employee"),
    path("admin_insight/", views.admin_insight_view, name="admin_insight"),
]