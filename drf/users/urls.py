from django.urls import include, path

from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view()),
    path('send/', views.FriendshipView.as_view({'post': 'sendRequest'})),
    path('friendsList/', views.FriendshipView.as_view({'get': 'friendsList'})),
    path('removeFriend/', views.FriendshipView.as_view({'post': 'removeFriend'})),
    path('sentRequestList/', views.FriendshipView.as_view({'get': 'sentRequestList'})),
    path('unreadRequestList/', views.FriendshipView.as_view({'get': 'unreadRequestList'})),
    path('unrejectedRequestList/', views.FriendshipView.as_view({'get': 'unrejectedRequestList'})),
    path('rejectedRequestList/', views.FriendshipView.as_view({'get': 'rejectedRequestList'})),
    path('acceptRequest/', views.FriendshipView.as_view({'post': 'acceptRequest'})),
    path('rejectRequest/', views.FriendshipView.as_view({'post': 'rejectRequest'})),
    path('stats/', views.StatisticsView.as_view())
]
