from django.urls import include, path

from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view()),
    path('send/', views.FriendshipViewTo.as_view({'post': 'sendRequest'})),
    path('friendsList/', views.FriendshipViewFrom.as_view({'get': 'friendsList'})),
    path('removeFriend/', views.FriendshipViewFrom.as_view({'post': 'removeFriend'})),
    path('sentRequestList/', views.FriendshipViewTo.as_view({'get': 'sentRequestList'})),
    path('unreadRequestList/', views.FriendshipViewFrom.as_view({'get': 'unreadRequestList'})),
    path('unrejectedRequestList/', views.FriendshipViewFrom.as_view({'get': 'unrejectedRequestList'})),
    path('rejectedRequestList/', views.FriendshipViewFrom.as_view({'get': 'rejectedRequestList'})),
    path('acceptRequest/', views.FriendshipViewFrom.as_view({'post': 'acceptRequest'})),
    path('rejectRequest/', views.FriendshipViewFrom.as_view({'post': 'rejectRequest'})),
    path('stats/', views.StatisticsView.as_view())
]
