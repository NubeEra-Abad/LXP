from django.urls import path
from learner import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('learnerclick', views.learnerclick_view),
path('learnerlogin', LoginView.as_view(template_name='learner/learnerlogin.html'),name='learnerlogin'),
path('learner-dashboard', views.learner_dashboard_view,name='learner-dashboard'),
]
