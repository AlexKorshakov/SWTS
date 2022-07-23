from django.urls import path

from .views import HomeViolations, ViewViolations, ViolationsByMainCategory, ViolationsByLocation, \
    ViolationsByGeneralContractor, ViolationsByIncidentLevel
from .views import test, simple_view, upload, delete_violations, upload_violations

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

    # запуск скрипта по нажатию кнопки из base.html
    path('upload/', upload, name='upload'),
    # запуск скрипта по нажатию кнопки из violations_detail.html
    path('update_violations/', upload_violations, name='update_violations'),
    path('delete_violations/', delete_violations, name='delete_violations'),

    path('test/', test, name='test'),
]

# To register this URLS
# path("core/", include("apps.core.web.urls"))
