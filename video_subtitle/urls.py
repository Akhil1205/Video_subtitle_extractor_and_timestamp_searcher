from django.urls import path
from .views import SearchSubtitlesView, VideoUploadView, LoginView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='upload'),
    path('search/', SearchSubtitlesView.as_view(), name='search'),
    path('login/', LoginView.as_view(), name='login'),
]
