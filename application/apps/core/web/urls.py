from django.template.context_processors import request
from django.urls import path

from .views import HomeViolations, ViewViolations, ViolationsByMainCategory, ViolationsByLocation, \
    ViolationsByGeneralContractor, ViolationsByIncidentLevel, ViolationsByStatus, user_login, user_logout, register, \
    post_edit, PostEdit
from .views import test, simple_view, upload_too_db_from_local_storage, delete_violations, update_violations

# Register your urls here

urlpatterns = [
    # path("", simple_view),
    path('', HomeViolations.as_view(), name='home'),
    path('violations/<int:pk>/', ViewViolations.as_view(),
         name='view_violations'),
    path('main_category/<int:main_category_id>/', ViolationsByMainCategory.as_view(),
         name='main_category'),
    path('location/<int:location_id>/', ViolationsByLocation.as_view(),
         name='location'),
    path('general_contractor/<int:general_contractor_id>/', ViolationsByGeneralContractor.as_view(),
         name='general_contractor'),
    path('incident_level/<int:incident_level_id>/', ViolationsByIncidentLevel.as_view(),
         name='incident_level'),
    path('status/<int:status_id>/', ViolationsByStatus.as_view(),
         name='status'),

    # запуск скрипта по нажатию кнопки из base.html
    path('upload/', upload_too_db_from_local_storage, name='upload'),
    # запуск скрипта по нажатию кнопки из violations_detail.html
    path('update_violations/', update_violations, name='update_violations'),

    path('post_edit/<int:violations_id>/', post_edit, name='post_edit'),

    path('delete_violations/', delete_violations, name='delete_violations'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('test/', test, name='test'),
]

# To register this URLS
# path("core/", include("apps.core.web.urls"))
