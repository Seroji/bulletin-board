from django.urls import path, include

from .views import (
    MainPageView,
    MainProfileView,
    MainProfileGetView,
    StatProfileGetView,
    TotalRepleisView,
    PostDetailView,
    FollowThePostView,
    LikeThePostView,
    ProfileChangeView,
    AfterChangeProfileView,
    PasswordEditView,
)


urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("profile/", MainProfileView.as_view(), name="main_profile"),
    path("replies/", TotalRepleisView.as_view(), name='total_replies'),
    path("detail/<int:pk>/", PostDetailView.as_view(), name='post_detail'),
    path('profile/change/', ProfileChangeView.as_view(), name='profile_change'),
    path('profile/paswword/', PasswordEditView.as_view(), name='password_change'),
]

htmx_patterns = [
    path("prof_main/", MainProfileGetView.as_view(), name='prof_partials_main'),
    path("prof_stat/", StatProfileGetView.as_view()),
    path('follower_change/', FollowThePostView.as_view(), name='follower_change'),
    path('like_change/', LikeThePostView.as_view(), name='like_change'),
    path('after_change/', AfterChangeProfileView.as_view(), name='after_change'),
]

urlpatterns += htmx_patterns
