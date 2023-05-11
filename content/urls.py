from django.urls import path, include

from .views import MainPageView, OwnProfileView, OwnProfileStaticticView


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('profile/', OwnProfileView.as_view(), name='own_profile'),
]

htmx_patterns = [
    path('statisctics/', OwnProfileStaticticView.as_view(), name='profile-statistics')
]

urlpatterns += htmx_patterns
