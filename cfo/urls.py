from django.urls import path
from cfo import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('cfoclick', views.cfoclick_view),
    path('cfologin', LoginView.as_view(template_name='cfo/cfologin.html'),name='cfologin'),
    path('cfo-dashboard', views.cfo_dashboard_view,name='cfo-dashboard'),

    path('cfo-coursetype', views.cfo_coursetype_view,name='cfo-coursetype'),
    path('cfo-add-coursetype', views.cfo_add_coursetype_view,name='cfo-add-coursetype'),
    path('cfo-update-coursetype/<int:pk>', views.cfo_update_coursetype_view,name='cfo-update-coursetype'),
    path('cfo-view-coursetype', views.cfo_view_coursetype_view,name='cfo-view-coursetype'),
    path('cfo-delete-coursetype/<int:pk>', views.cfo_delete_coursetype_view,name='cfo-delete-coursetype'),
]
