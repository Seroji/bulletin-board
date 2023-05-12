from django.urls import path, include

from .views import (
    MainPageView,
    MainProfileView,
    MainProfileGetView,
    StatProfileGetView,
    TotalRepleisView,
)


urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("profile/", MainProfileView.as_view(), name="main_profile"),
    path("replies/", TotalRepleisView.as_view(), name='total_replies'),
]

htmx_patterns = [
    path("prof_main", MainProfileGetView.as_view()),
    path("prof_stat", StatProfileGetView.as_view()),
]

urlpatterns += htmx_patterns
