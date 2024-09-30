from typing import Union

from django.urls import URLPattern, URLResolver, path, include
# import django.contrib.auth.urls

from accounts.views import ProfileView, SignupView, ConfirmView

app_name: str = "accounts"

urlpatterns: list[Union[URLPattern, URLResolver]] = [
    path('', include('django.contrib.auth.urls')),
    path('confirm/', ConfirmView.as_view(), name="confirm"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('signup/', SignupView.as_view(), name="signup"),
]
