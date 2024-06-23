from django.urls import path
from .views import SearchView, VideoUploadView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='upload'),
    path('success/', SearchView.as_view(), name='success'),
]
