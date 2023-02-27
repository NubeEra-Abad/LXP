from django.urls import path
from learner import views
urlpatterns = [
path('learnerclick', views.learnerclick_view),
path('learner-dashboard', views.learner_dashboard_view,name='learner-dashboard'),
]
