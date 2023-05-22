from django.urls import path, include

from .views import (
    MainPageView,
    MainProfileView,
    MainProfileGetView,
    StatProfileGetView,
    TotalRepliesView,
    PostDetailView,
    FollowThePostView,
    LikeThePostView,
    ProfileChangeView,
    AfterChangeProfileView,
    PasswordEditView,
    PostAddView,
    ReplyActionView,
    VerifyEmailByCodeView,
    ChangePostView,
    FavouritePostView,
    AdvertismentView
)


urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("profile/", MainProfileView.as_view(), name="main_profile"),
    path("replies/", TotalRepliesView.as_view(), name='total_replies'),
    path("detail/<int:pk>/", PostDetailView.as_view(), name='post_detail'),
    path('profile/change/', ProfileChangeView.as_view(), name='profile_change'),
    path('profile/paswword/', PasswordEditView.as_view(), name='password_change'),
    path('add/', PostAddView.as_view(), name='post_add'),
    path('verify/', VerifyEmailByCodeView.as_view(), name='verify_email'),
    path('change/<int:pk>', ChangePostView.as_view(), name='change_post'),
    path('favourite/', FavouritePostView.as_view(), name='post_favourite'),
    path('advertisment/', AdvertismentView.as_view(), name='advertisment')
]

htmx_patterns = [
    path("prof_main/", MainProfileGetView.as_view(), name='prof_partials_main'),
    path("prof_stat/", StatProfileGetView.as_view()),
    path('follower_change/', FollowThePostView.as_view(), name='follower_change'),
    path('like_change/', LikeThePostView.as_view(), name='like_change'),
    path('after_change/', AfterChangeProfileView.as_view(), name='after_change'),
    path('reply_action/', ReplyActionView.as_view(), name='reply_action')
]

urlpatterns += htmx_patterns
