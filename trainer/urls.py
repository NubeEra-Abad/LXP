from django.urls import path
from trainer import views
from django.contrib.auth.views import LoginView

urlpatterns = [

path('trainerclick', views.trainerclick_view),
path('trainerlogin', LoginView.as_view(template_name='trainer/trainerlogin.html'),name='trainerlogin'),
path('trainer-dashboard', views.trainer_dashboard_view,name='trainer-dashboard'),


]
