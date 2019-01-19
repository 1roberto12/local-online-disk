from django.urls import include, path

from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view()),
    path('send/', views.FriendshipView.as_view({'post': 'sendRequest'})),
    path('friendsList/', views.FriendshipView.as_view({'get': 'friendsList'})),
    path('removeFriend/', views.FriendshipView.as_view({'post': 'removeFriend'})),
    path('sentRequestList/', views.FriendshipView.as_view({'get': 'sentRequestList'})),
]
