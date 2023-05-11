from django.urls import path, include

from .views import MainPageView, OwnProfileView


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('profile/', OwnProfileView.as_view(), name='own_profile'),
]
