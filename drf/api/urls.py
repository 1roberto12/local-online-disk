from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('files/', views.FileInfoViewSet.as_view({'get': 'list'})),
    path('files/<path:p>', views.FileInfoViewSet.as_view({'get': 'list'})),
    path('file/get/<path:p>', views.FileInfoViewSet.as_view({'get': 'download', 'post': 'create', 'delete': 'destroy'})),
    path('file/get/', views.FileInfoViewSet.as_view({'get': 'download', 'post': 'create'})),
]
