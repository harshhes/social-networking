from django.urls import path

from .views import (
    RegisterUserView,
    LoginUserView,
    ListUsersView,
    SearchUserView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    PendingRequestsView,
    AcceptedRequestsView,

    )

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("login/", LoginUserView.as_view(), name='register'),
    path("list_users/", ListUsersView.as_view(), name='list_users'),
    path("search_users/", SearchUserView.as_view(), name='search_users'),
    
    path("send_request/", SendFriendRequestView.as_view(), name='send_request'),
    path("accept_request/<int:pk>/", AcceptFriendRequestView.as_view(), name='accept_request'),
    path("reject_request/<int:pk>/", RejectFriendRequestView.as_view(), name='reject_request'),

    path("pending_requests/", PendingRequestsView.as_view(), name='pending_requests'),
    path("list_friends/", AcceptedRequestsView.as_view(), name='accepted_requests'),

]