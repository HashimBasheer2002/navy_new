from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('veteran-profile/', views.create_or_update_profile, name='veteran_profile'),
    path('experiences/', views.share_experience, name='veteran_experiences'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('course/create/', views.create_course, name='create_course'),
    #add veteranprofile

    path('course/', views.view_course, name='view_course'),
    path('member/',views.memebership,name='member'),
    path('create/', views.create_mock_test, name='create_mock_test'),
    path('<int:test_id>/add-question/', views.add_question, name='add_question'),
    path('testlist/', views.mock_test_list, name='mock_test_list'),
    path('<int:test_id>/attempt/', views.take_test, name='take_test'),
    path('<int:test_id>/result/', views.test_result, name='test_result'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('deletetest/',views.delete_test,name='delete_test'),
    path('add-news/', views.add_news, name='add_news'),
    path('news/', views.view_news, name='news_list'),
    path('applications/', views.applications, name='applications'),

    #add study meterials

    #add wall of honour
    path('wall-of-honor/', views.wall_of_honor, name='wall_of_honor'),
    path('wall-of-honor/post/', views.post_wall_entry, name='post_wall_entry'),
    path('wall-of-honor/<int:entry_id>/add-media/', views.add_wall_media, name='add_wall_media'),
]




