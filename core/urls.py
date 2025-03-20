from django.urls import path
from . import views

urlpatterns = [
    path('/home', views.home, name='home'),
    path('', views.index, name='index'),
    path('/about', views.about, name='about'),

    path('study-materials/', views.study_materials, name='study_materials'),
    path('add-study-material/', views.add_study_material, name='add_study_material'),
    path('course/<int:course_id>/applicants/', views.course_applicants, name="course_applicants"),
    path("users_list/", views.user_list, name="user_list"),
    path('veterans/', views.list_veterans, name='veteran_list'),
    path('veterans/<int:pk>/', views.view_veteran_profile, name='view_veteran_profile'),

    path("subscribe/", views.subscribe, name="subscribe"),
    path("create-order/", views.create_order, name="create_order"),
    path("verify-payment/", views.payment_success, name="verify_payment"),
    path('purchase/<int:course_id>/', views.buy_course, name='purchase_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
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
    path('deletetest/<int:test_id>/', views.delete_test, name='delete_test'),
    path('add-news/', views.add_news, name='add_news'),
    path('news/', views.view_news, name='news_list'),
    path('applications/', views.applications, name='applications'),

    #add study meterials

    #add wall of honour
    path('wall-of-honor/', views.wall_of_honor, name='wall_of_honor'),
    path('wall-of-honor/post/', views.post_wall_entry, name='post_wall_entry'),
    path('wall-of-honor/<int:entry_id>/add-media/', views.add_wall_media, name='add_wall_media'),
    path('create-payment/<int:material_id>/', views.create_payment, name='create_payment'),
    path('payment-success/<int:material_id>/', views.payment_success, name='payment_success'),
    path('razorpay-payment/<int:material_id>/', views.razorpay_payment, name='razorpay_payment'),
    path('mock-test-results/', views.mock_test_results, name='mock_test_results'),
    path('suggest-improvement/<int:result_id>/', views.suggest_improvement, name='suggest_improvement'),
    path('my-books/', views.my_books, name='my_books'),
    path("campaigns/", views.view_campaigns, name="view_campaigns"),
    path("campaigns/<int:campaign_id>/participate/", views.participate_campaign, name="participate_campaign"),

    # Admin URLs
    path("add/campaigns/", views.add_campaign, name="admin_campaigns"),
    path("campaigns/edit/<int:campaign_id>/", views.edit_campaign, name="edit_campaign"),
    path("campaigns/delete/<int:campaign_id>/", views.delete_campaign, name="delete_campaign"),
    path("campaigns/<int:campaign_id>/participants/", views.view_participants, name="view_participants"),

    path('users/<int:user_id>/profile/', views.view_profile, name='view_profile'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('suggest-improvement/<int:result_id>/', views.suggest_improvement, name='suggest_improvement'),
    path('my-suggestions/', views.user_suggestions, name='user_suggestions'),
    path('upload-question-bank/', views.upload_question_bank, name='upload_question_bank'),
    path('question-bank/', views.question_bank_list, name='question_bank_list'),

]







