from django.template.context_processors import request
from django.urls import path

from .views import (HomeRegisterActsPrescriptions,
                    HomeRegisterNormativeDocuments, HomeRegisterUnclosedPoints,
                    HomeViolations, PostEdit, ViewViolations,
                    ViolationsByFinished, ViolationsByGeneralContractor,
                    ViolationsByIncidentLevel, ViolationsByMainCategory,
                    ViolationsByMainLocation, ViolationsByStatus,
                    ViolationsByWeek, add_violations, delete_violations,
                    post_edit, register, simple_view, statistic, test,
                    update_violations, upload_too_db_from_local_storage,
                    user_login, user_logout)

# Register your urls here

urlpatterns = [
    # path("", simple_view),
    path('', HomeViolations.as_view(),
         name='home'),
    path('register_acts_prescriptions', HomeRegisterActsPrescriptions.as_view(),
         name='register_acts_prescriptions'),
    path('register_normative_documents', HomeRegisterNormativeDocuments.as_view(),
         name='register_normative_documents'),
    path('register_of_unclosed_points', HomeRegisterUnclosedPoints.as_view(),
         name='register_of_unclosed_points'),


    path('violations/<int:pk>/', ViewViolations.as_view(),
         name='view_violations'),
    path('main_category/<int:main_category_id>/', ViolationsByMainCategory.as_view(),
         name='main_category'),
    path('main_location/<int:main_location_id>/', ViolationsByMainLocation.as_view(),
         name='main_location'),
    path('general_contractor/<int:general_contractor_id>/', ViolationsByGeneralContractor.as_view(),
         name='general_contractor'),
    path('incident_level/<int:incident_level_id>/', ViolationsByIncidentLevel.as_view(),
         name='incident_level'),
    path('status/<int:status_id>/', ViolationsByStatus.as_view(),
         name='status'),
    path('finished/<int:finished_id>/', ViolationsByFinished.as_view(),
         name='finished'),
    path('view_violations_by_week/<int:week_id>/', ViolationsByWeek.as_view(),
         name='week'),

    # запуск скрипта по нажатию кнопки из base.html
    path('upload/', upload_too_db_from_local_storage, name='upload'),
    path('statistic/', statistic, name='statistic'),
    # запуск скрипта по нажатию кнопки из violations_detail.html

    path('post_edit/<int:violations_id>/', post_edit, name='post_edit'),

    path('update_violations/', update_violations, name='update_violations'),
    path('delete_violations/', delete_violations, name='delete_violations'),
    path('add_violations/', add_violations, name='add_violations'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('test/', test, name='test'),
    # path('test/', HomeRegisterActsPrescriptions.as_view(), name='test'),
]

# To register this URLS
# path("core/", include("apps.core.web.urls"))
