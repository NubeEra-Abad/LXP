from django.urls import path
from cfo import views
from django.contrib.auth.views import LoginView

urlpatterns = [

path('cfoclick', views.cfoclick_view),
path('cfologin', LoginView.as_view(template_name='cfo/cfologin.html'),name='cfologin'),
path('cfo-dashboard', views.cfo_dashboard_view,name='cfo-dashboard'),
]
