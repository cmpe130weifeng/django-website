from django.urls import include, path
from employee_page import views

app_name = 'employee_page'

urlpatterns = [
    path("", views.index, name = "index"),
    path("insight/<int:dept_id>/", views.request_insight, name = "request_insight"),
    
]