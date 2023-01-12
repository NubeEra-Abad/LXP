from django.urls import path
from cto import views
from django.contrib.auth.views import LoginView
from cto.views import CreateCrudUser, CrudView, DeleteCrudUser, UpdateCrudUser,CtoCourseView
urlpatterns = [

    path('ctoclick', views.ctoclick_view),
    path('ctologin', LoginView.as_view(template_name='cto/ctologin.html'),name='ctologin'),
    path('cto-dashboard', views.cto_dashboard_view,name='cto-dashboard'),

    path('cto-subject', views.cto_subject_view,name='cto-subject'),
    path('cto-add-subject', views.cto_add_subject_view,name='cto-add-subject'),
    path('cto-update-subject/<int:pk>', views.cto_update_subject_view,name='cto-update-subject'),
    path('cto-view-subject', views.cto_view_subject_view,name='cto-view-subject'),
    path('cto-delete-subject/<int:pk>', views.cto_delete_subject_view,name='cto-delete-subject'),

    path('cto-chapter', views.cto_chapter_view,name='cto-chapter'),
    path('cto-add-chapter', views.cto_add_chapter_view,name='cto-add-chapter'),
    path('cto-update-chapter/<int:pk>', views.cto_update_chapter_view,name='cto-update-chapter'),
    path('cto-view-chapter', views.cto_view_chapter_view,name='cto-view-chapter'),
    path('cto-delete-chapter/<int:pk>', views.cto_delete_chapter_view,name='cto-delete-chapter'),

    path('cto-topic', views.cto_topic_view,name='cto-topic'),
    path('cto-add-topic', views.cto_add_topic_view,name='cto-add-topic'),
    path('cto-add-defualt-topic', views.cto_add_defualt_topic_view,name='cto-add-defualt-topic'),
    path('cto-update-topic/<int:pk>', views.cto_update_topic_view,name='cto-update-topic'),
    path('cto-view-topic', views.cto_view_topic_view,name='cto-view-topic'),
    path('cto-delete-topic/<int:pk>', views.cto_delete_topic_view,name='cto-delete-topic'),

    path('cto-course', views.cto_course_view,name='cto-course'),
    path('cto-add-course', views.cto_add_course_view,name='cto-add-course'),
    path('cto-view-course', views.cto_view_course_view,name='cto-view-course'),
    path('cto-update-course/<int:pk>', views.cto_update_course_view,name='cto-update-course'),
    path('cto-view-course-details/<cname>/<int:cid>', views.cto_view_course_details_view,name='cto-view-course-details'),
    path('cto-delete-course/<int:pk>', views.cto_delete_course_view,name='cto-delete-course'),

    path('cto-add-course-by-playlist', views.cto_add_course_by_playlist_view,name='cto-add-course-by-playlist'),

    path('course-list', views.CourseList.as_view(), name='course-list'),
    path('course-add', views.CDetailsCreate.as_view(), name='course-add'),
    path('course-update/<int:pk>', views.CDetailsUpdate.as_view(), name='course-update'),
    path('course-delete/<int:pk>', views.courseDelete.as_view(), name='course-delete'),

    path('cto-passionateskill', views.cto_passionateskill_view,name='cto-passionateskill'),
    path('cto-add-passionateskill', views.cto_add_passionateskill_view,name='cto-add-passionateskill'),
    path('cto-update-passionateskill/<int:pk>', views.cto_update_passionateskill_view,name='cto-update-passionateskill'),
    path('cto-view-passionateskill', views.cto_view_passionateskill_view,name='cto-view-passionateskill'),
    path('cto-delete-passionateskill/<int:pk>', views.cto_delete_passionateskill_view,name='cto-delete-passionateskill'),

    path('cto-knownskill', views.cto_knownskill_view,name='cto-knownskill'),
    path('cto-add-knownskill', views.cto_add_knownskill_view,name='cto-add-knownskill'),
    path('cto-update-knownskill/<int:pk>', views.cto_update_knownskill_view,name='cto-update-knownskill'),
    path('cto-view-knownskill', views.cto_view_knownskill_view,name='cto-view-knownskill'),
    path('cto-delete-knownskill/<int:pk>', views.cto_delete_knownskill_view,name='cto-delete-knownskill'),

    path('cto-sync-youtube', views.cto_sync_youtube_view,name='cto-sync-youtube'),
    path('cto-sync-youtube-start', views.cto_sync_youtube_start_view,name='cto-sync-youtube-start'),
    path('cto-sync-youtube-byselected-playlist-start', views.cto_sync_youtube_byselected_playlist_start_view,name='cto-sync-youtube-byselected-playlist-start'),
    
    path('courses', views.courses,name='courses'),
    path('modules', views.modules, name='modules'),

    # Django Ajax CRUD Operations
    path('crudcto/', CrudView.as_view(), name='crud_ajaxcto'),
    path('ajax/crudcto/create/', CreateCrudUser.as_view(), name='cto_crud_ajax_create'),
    path('ajax/crudcto/delete/', DeleteCrudUser.as_view(), name='cto_crud_ajax_delete'),
    path('ajax/crudcto/update/', UpdateCrudUser.as_view(), name='cto_crud_ajax_update'),

    path('ctocourse', views.CtoCourseView,name='ctocourse'),
    path('ajax/crudcto/create/', CreateCrudUser.as_view(), name='cto_crud_ajax_create'),
    path('ajax/crudcto/delete/', DeleteCrudUser.as_view(), name='cto_crud_ajax_delete'),
    path('ajax/crudcto/update/', UpdateCrudUser.as_view(), name='cto_crud_ajax_update'),
    path('modules1', views.Cto_Course_View, name='modules1'),

]
