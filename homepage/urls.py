from django.urls import include, path
from homepage import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = 'homepage'

urlpatterns = [
    path("", views.index, name = "index"),
    path("log_in/", views.login_view, name = "log_in"),
    path("log_out/", views.user_logout, name = "log_out"),
    path("about/", TemplateView.as_view(template_name="about.html"), name = "about"),
    

    
]