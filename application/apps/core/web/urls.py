from django.urls import path

from .views import HomeViolations, test, ViewViolations, NewsByMainCategory
from .views import test, simple_view

# Register your urls here

urlpatterns = [
    # path("", simple_view),
    path('', HomeViolations.as_view(), name='home'),
    path('test/', test, name='test'),
    path('violations/<int:pk>/', ViewViolations.as_view(), name='view_violations'),
    # path('category/<int:category_id>/', NewsByMainCategory.as_view(extra_context={'title': 'Категория хз'}),
    #      name='main_category'),
]

# To register this URLS
# path("core/", include("apps.core.web.urls"))
