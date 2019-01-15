from django.urls import include, path

from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view()),
    path('send/', views.FriendshipView.as_view({'post': 'sendRequest'})),
    path('friendslist/', views.FriendshipView.as_view({'get': 'friendsList'})),
    path('removefriend/', views.FriendshipView.as_view({'post': 'removeFriend'})),
    path('sentRequestList/', views.FriendshipView.as_view({'get': 'sentRequestList'})),
]
