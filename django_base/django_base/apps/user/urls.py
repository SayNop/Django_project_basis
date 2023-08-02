from django.conf.urls import url

from .views import passport


urlpatterns = [
    url(r'register$', passport.RegisterView.as_view()),
    url(r'login$', passport.PhoneLoginView.as_view())
]
