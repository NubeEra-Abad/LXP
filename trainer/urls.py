from django.urls import path
from trainer import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('trainer-dashboard', views.trainer_dashboard_view,name='trainer-dashboard'),
    path('trainer-material', views.trainer_material_view,name='trainer-material'),
    path('trainer-add-material', views.trainer_add_material_view,name='trainer-add-material'),
    path('trainer-update-material/<int:pk>', views.trainer_update_material_view,name='trainer-update-material'),
    path('trainer-view-material', views.trainer_view_material_view,name='trainer-view-material'),
    path('trainer-delete-material/<int:pk>', views.trainer_delete_material_view,name='trainer-delete-material'),
    path('trainer-show-material/<materialtype>,/<int:pk>', views.trainer_show_material_view,name='trainer-show-material'),

    path('trainer-material-upload-file', views.trainer_material_upload_file_view,name='trainer-material-upload-file'),
    path('trainer-material-start-upload-file', views.trainer_material_start_upload_file_view,name='trainer-material-start-upload-file'),
]
