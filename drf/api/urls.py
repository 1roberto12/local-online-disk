from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('files/', views.FileInfoView.as_view()),
    path('files/<path:p>', views.FileInfoView.as_view()),
    # path('file/get/<path:p>', views.FileInfoViewSet.as_view({'get': 'download', 'post': 'create', 'delete': 'destroy'})),
    # path('file/get/', views.FileInfoViewSet.as_view({'get': 'download', 'post': 'create'})),
    path('share/', views.FileSharingView.as_view()),
    path('share/my/', views.FileSharingView.as_view()),
    path('share/<uuid:id>', views.FileSharingView.as_view()),
    path('share/<uuid:id>/<path:p>', views.FileSharingView.as_view()),
]
