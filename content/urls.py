from django.urls import path, include

from .views import (
    MainPageView,
    MainProfileView,
    MainProfileGetView,
    StatProfileGetView,
    TotalRepleisView,
    PostDetailView,
    FollowThePostView
)


urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("profile/", MainProfileView.as_view(), name="main_profile"),
    path("replies/", TotalRepleisView.as_view(), name='total_replies'),
    path("detail/<int:pk>/", PostDetailView.as_view(), name='post_detail'),
]

htmx_patterns = [
    path("prof_main/", MainProfileGetView.as_view()),
    path("prof_stat/", StatProfileGetView.as_view()),
    path('follower_change/', FollowThePostView.as_view(), name='follower_change'),
]

urlpatterns += htmx_patterns
